import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
import json
import random

from decouple import config
# Configure OpenAI API key
# store_id = config('store_id')
# OPENAI_API_KEY = config('OPENAI_API_KEY')
# openai_client = OpenAI(api_key=OPENAI_API_KEY)
class PCBuilderAPIView(APIView):
    """
    AI-powered PC Builder using reduced CSV data and JSON responses.
    """

    def load_csv_data(self, file_path):
        """
        Helper function to load data from a CSV file.
        """
        pc_parts = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['price'] = float(row['price'])
                row['stock_quantity'] = int(row['stock_quantity'])
                pc_parts.append(row)
        return pc_parts

    def sample_csv_data(self, pc_parts, max_entries_per_category=10):
        """
        Reduce the dataset size by sampling a fixed number of entries per category.
        """
        sampled_parts = []
        categories = set([part['category'] for part in pc_parts])

        for category in categories:
            category_parts = [part for part in pc_parts if part['category'] == category]
            sampled_parts.extend(
                random.sample(category_parts, min(len(category_parts), max_entries_per_category))
            )

        return sampled_parts

    def post(self, request, *args, **kwargs):
        """
        Handle user inputs like budget, usage, and preferences.
        """
        try:
            # OPENAI_API_KEY = config('OPENAI_API_KEY')
            OPENAI_API_KEY = config('OPENAI_API_KEY')

            openai_client = OpenAI(api_key=OPENAI_API_KEY)
            # Extract inputs from the request
            budget = float(request.data.get("budget", 0))
            usage = request.data.get("usage", "").strip()
            additional_preferences = request.data.get("preferences", "").strip()

            if not budget or not usage:
                return Response(
                    {"error": "Budget and usage are required fields."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Load PC parts data from the CSV file
            file_path = "api/ecom/pc_parts_realistic_bdt.csv"  # Adjust the path as necessary
            pc_parts = self.load_csv_data(file_path)

            # Sample data to reduce size
            pc_parts = self.sample_csv_data(pc_parts, max_entries_per_category=10)

            # Prepare reduced context for OpenAI
            context = "\n".join(
                [
                    f"{part['category']}: {part['name']} - Brand: {part['brand']}, "
                    f"Price: ৳{part['price']}, Description: {part['description']}"
                    for part in pc_parts
                ]
            )

            # Generate recommendations using OpenAI with JSON response format
            prompt = f"""
            
            User needs to build a PC for {usage} within a budget of ৳{budget}. Remember, Total Price
            Should not be more than the budget. 
            Available PC Parts(Context):\n{context}\n\n
            Suggest essential components (CPU, GPU, RAM, Storage, PSU, Case, Motherboard, etc.) 
            and explain why they are chosen. Also, give the response as per the context. Use approximate price breakdowns and ensure the response is formatted as JSON:
            
            {{
                "recommendations": [
                    {{"category": "", "name": "", "reason": "", "price": ""}}
                ],
                "total_price": ""
            }}.
            
            """
            if additional_preferences:
                prompt += f" Additional preferences: {additional_preferences}."

            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                max_tokens=4000,  # Adjust tokens limit for safety
                response_format={"type": "json_object"},
                messages=[{"role": "user", "content": prompt}],
            )
            query_response = response.choices[0].message.content

            # Parse JSON response from OpenAI
            try:
                parsed_response = json.loads(query_response)
            except json.JSONDecodeError:
                return Response(
                    {"error": "Failed to parse JSON from OpenAI response."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Log and check if reasons are correct
            for rec in parsed_response.get("recommendations", []):
                print(f"Category: {rec['category']}, Name: {rec['name']}, Reason: {rec['reason']}")

            # Response data
            response_data = {
                "recommendations": parsed_response.get("recommendations", []),
                "total_price": parsed_response.get("total_price", 0),
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
