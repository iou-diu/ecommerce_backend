import random
import os
from django.conf import settings
from django.core.management.base import BaseCommand

import barcode
from barcode.writer import ImageWriter
from ecom.models import ProductStock
from django.core.exceptions import ValidationError

class Command(BaseCommand):
    help = 'Generate or validate 12-digit UPC codes for ProductStock'

    def handle(self, *args, **kwargs):
        stocks = ProductStock.objects.all()

        for stock in stocks:
            if stock.upc:
                if len(stock.upc) != 12 or not stock.upc.isdigit():
                    self.stdout.write(self.style.WARNING(f'Invalid UPC ({stock.upc}) for SKU {stock.sku}. Regenerating...'))
                    stock.upc = self.generate_upc()
                    stock.save()
                    self.stdout.write(self.style.SUCCESS(f'UPC for {stock.sku} regenerated as {stock.upc}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'UPC for {stock.sku} is valid.'))
            else:
                # Generate UPC if not provided
                stock.upc = self.generate_upc()
                stock.save()
                self.stdout.write(self.style.SUCCESS(f'UPC for {stock.sku} generated as {stock.upc}'))

        self.stdout.write(self.style.SUCCESS('Finished validating/generating UPCs.'))

    def generate_upc(self):
        """
        Generate a valid 12-digit UPC.
        The first 11 digits are randomly generated, and the 12th is a check digit.
        """
        base_code = [random.randint(0, 9) for _ in range(11)]  # First 11 digits
        check_digit = self.calculate_check_digit(base_code)
        return ''.join(map(str, base_code)) + str(check_digit)

    def calculate_check_digit(self, base_code):
        """
        Calculate the check digit for the UPC using the first 11 digits.
        Formula: (sum of odd-position digits * 3 + sum of even-position digits) modulo 10
        """
        odd_sum = sum(base_code[i] for i in range(0, 11, 2))  # Odd-position digits
        even_sum = sum(base_code[i] for i in range(1, 11, 2))  # Even-position digits
        total = (odd_sum * 3) + even_sum
        check_digit = (10 - (total % 10)) % 10
        return check_digit
    
    def generate_barcode_image(self, upc, sku):
        """
        Generate a barcode image from the UPC and save it as a PNG file.
        The image will be saved in the 'media/barcodes' directory.
        """
        # Define the path to save barcode images
        barcode_dir = os.path.join(settings.MEDIA_ROOT, 'barcodes')
        if not os.path.exists(barcode_dir):
            os.makedirs(barcode_dir)

        # Create the barcode using the UPC-A format
        upc_barcode = barcode.get('upc', upc, writer=ImageWriter())

        # Save the barcode as a PNG image
        barcode_filename = f'{sku}.png'
        barcode_filepath = os.path.join(barcode_dir, barcode_filename)
        upc_barcode.save(barcode_filepath)

        self.stdout.write(self.style.SUCCESS(f'Barcode image for SKU {sku} saved at {barcode_filepath}'))