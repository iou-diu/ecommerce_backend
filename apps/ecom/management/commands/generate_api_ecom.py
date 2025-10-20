import os
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import models  # Import the models module

def add_import_if_missing(file_path, import_statement):
    """Adds an import statement to the file if it's not already present."""
    with open(file_path, 'r') as file:
        content = file.read()

    if import_statement not in content:
        with open(file_path, 'a') as file:
            file.write(f"\n{import_statement}\n")

class Command(BaseCommand):
    help = 'Generate DRF ViewSets, Serializers, and URL router for a given model'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Indicates the model name for which the API will be generated')

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name']
        try:
            model = apps.get_model('ecom', model_name)
        except LookupError:
            self.stdout.write(self.style.ERROR(f'Model "{model_name}" not found in ecom'))
            return

        # Generate API files
        self.generate_viewsets(model)
        self.generate_serializers(model)
        self.generate_urls(model)
        self.stdout.write(self.style.SUCCESS(f'Successfully generated API for {model_name}'))

    def generate_viewsets(self, model):
        model_name = model.__name__
        viewsets_file = "api/ecom/views.py"

        # Add imports if missing
        imports = [
            'from rest_framework import viewsets',
            'from rest_framework.response import Response',
            'from rest_framework.permissions import IsAuthenticated',
            'from django_filters.rest_framework import DjangoFilterBackend',
            'from rest_framework.filters import SearchFilter',
            f'from .serializers import {model_name}Serializer',
            f'from apps.ecom.models import {model_name}'
        ]
        for import_statement in imports:
            add_import_if_missing(viewsets_file, import_statement)

        # Exclude file fields from filterset_fields
        filter_fields = [f.name for f in model._meta.fields if not isinstance(f, (models.FileField, models.ImageField))]
        filter_fields_str = ", ".join([f"'{field}'" for field in filter_fields])

        # Construct the ViewSet content
        viewset_content = [
            "",
            f"class {model_name}ViewSet(viewsets.ModelViewSet):",
            f"    queryset = {model_name}.objects.all().order_by('-id')",
            f"    serializer_class = {model_name}Serializer",
            "    permission_classes = [IsAuthenticated]",  # Modify based on your requirements
            "    filter_backends = [DjangoFilterBackend, SearchFilter]",
            f"    filterset_fields = [{filter_fields_str}]",  # Add your filtered fields dynamically
            "    search_fields = ['name', 'description']",  # Customize based on your model fields
            "",
            "    def retrieve(self, request, *args, **kwargs):",
            f"        instance = self.get_object()",
            "        serializer = self.get_serializer(instance)",
            "        return Response(serializer.data)",
        ]

        # Append the viewset content to the views file
        with open(viewsets_file, 'a') as file:
            file.write("\n".join(viewset_content) + "\n")

    def generate_serializers(self, model):
        model_name = model.__name__
        serializers_file = "api/ecom/serializers.py"

        # Add imports if missing
        imports = [
            'from rest_framework import serializers',
            f'from apps.ecom.models import {model_name}'
        ]
        for import_statement in imports:
            add_import_if_missing(serializers_file, import_statement)

        # Exclude file fields from the serializer fields
        fields = [f.name for f in model._meta.fields if not isinstance(f, (models.FileField, models.ImageField))]
        fields_str = ", ".join([f"'{field}'" for field in fields])

        # Create the serializer content
        serializer_content = [
            "",
            f"class {model_name}Serializer(serializers.ModelSerializer):",
            "    class Meta:",
            f"        model = {model_name}",
            f"        fields = [{fields_str}]"
        ]

        # Append the serializer content to the serializers file
        with open(serializers_file, 'a') as file:
            file.write("\n".join(serializer_content) + "\n")

    def generate_urls(self, model):
        model_name = model.__name__.lower()
        urls_file = "api/urls.py"

        # Add imports if missing
        add_import_if_missing(urls_file, 'from rest_framework.routers import DefaultRouter')
        viewset_imports = f"from api.ecom.views import {model.__name__}ViewSet"

        # Read the current content of urls.py
        with open(urls_file, 'r') as file:
            content = file.readlines()

        # Check if the necessary import already exists and add it at the top if it's missing
        if viewset_imports not in "".join(content):
            for index, line in enumerate(content):
                if not line.startswith("from") and not line.startswith("import"):
                    content.insert(index, viewset_imports + "\n")
                    break

        # Ensure router definition exists
        router_defined = False
        for line in content:
            if 'router = DefaultRouter()' in line:
                router_defined = True
                break

        if not router_defined:
            # Insert the router definition at the correct location if not already present
            content.insert(len(content), "\nrouter = DefaultRouter()\n")

        # Add the route to the existing router
        route = f"router.register(r'{model_name}', {model.__name__}ViewSet, basename='{model_name}')"
        if route not in "".join(content):
            # Find the appropriate place to insert the new route before urlpatterns
            for index, line in enumerate(content):
                if 'urlpatterns' in line:
                    content.insert(index, f"{route}\n")
                    break

        # Write the updated content back to urls.py
        with open(urls_file, 'w') as file:
            file.writelines(content)

