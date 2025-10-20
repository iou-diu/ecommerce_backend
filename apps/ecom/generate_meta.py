import json
from decouple import config
from django.http import JsonResponse
import openai
from django.views.decorators.csrf import csrf_exempt

# Set OpenAI API key
from openai import OpenAI
OPENAI_API_KEY = config('OPENAI_API_KEY')

@csrf_exempt
def generate_meta(request):
    if request.method == "POST":
        try:
            openai_client = OpenAI(api_key=OPENAI_API_KEY)
            data = json.loads(request.body)
            name = data.get("name", "")
            description = data.get("description", "")
            key_features = data.get("key_features", "")
            category = data.get("category", "")
            brand = data.get("brand", "")
            warranty = data.get("warranty", "")

            # Prompt for OpenAI
            prompt = f"""
            Consider yourself an SEO expert. Generate a meta title and description for the following product details:
            Name: {name}
            Description: {description}
            Key Features: {key_features}
            Category: {category}
            Brand: {brand}
            Warranty: {warranty}

            Response should be in JSON format:
            {{
                "meta_title": "<Meta Title>",
                "meta_description": "<Meta Description>"
            }}

            Ensure:
            - The Meta Description does not exceed 155 characters.
            - The Meta Title is below 60 characters.
            """

            # Call OpenAI API
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                max_tokens=2000,  # Adjust tokens limit for safety
                response_format={"type": "json_object"},
                messages=[{"role": "user", "content": prompt}],
            )
            query_response = response.choices[0].message.content

            meta_data = json.loads(query_response)

            return JsonResponse(meta_data)

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def generate_meta_category(request):
    if request.method == "POST":
        try:

            openai_client = OpenAI(api_key=OPENAI_API_KEY)
            data = json.loads(request.body)
            name = data.get("name", "")
            description = data.get("description", "")
            parent = data.get("parent", "")

            # Prompt for OpenAI
            prompt = f"""
            Consider yourself an SEO expert. Generate a meta title and description for the following category details:
            Name: {name}
            Description: {description}
            Parent Category: {parent}

            Response should be in JSON format:
            {{
                "meta_title": "<Meta Title>",
                "meta_description": "<Meta Description>"
            }}

            Ensure:
            - The Meta Description does not exceed 155 characters.
            - The Meta Title is below 60 characters.
            """

            # Call OpenAI API
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                max_tokens=2000,  # Adjust tokens limit for safety
                response_format={"type": "json_object"},
                messages=[{"role": "user", "content": prompt}],
            )
            query_response = response.choices[0].message.content
            meta_data = json.loads(query_response)

            return JsonResponse(meta_data)

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"},status=400)
