import os
from django.core.management.base import BaseCommand
from django.apps import apps

def add_import_if_missing(file_path, import_statement):
    """Adds an import statement to the file if it's not already present."""
    with open(file_path, 'r') as file:
        content = file.read()

    if import_statement not in content:
        with open(file_path, 'a') as file:
            file.write(f"\n{import_statement}\n")

class Command(BaseCommand):
    help = 'Generate CRUD operations for a given model'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Indicates the model name for which CRUD will be generated')

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name']
        try:
            model = apps.get_model('ecom', model_name)
        except LookupError:
            self.stdout.write(self.style.ERROR(f'Model "{model_name}" not found in ecom'))
            return

        # Generate CRUD files
        self.generate_views(model)
        self.generate_forms(model)
        self.generate_filters(model)
        self.generate_tables(model)
        self.generate_urls(model)
        self.stdout.write(self.style.SUCCESS(f'Successfully generated CRUD for {model_name}'))

    def generate_views(self, model):
        model_name = model.__name__
        views_file = "apps/ecom/views.py"

        # Add imports if missing
        imports = [
            'from django.contrib.auth.mixins import LoginRequiredMixin',
            'from django.views.generic import ListView, CreateView, UpdateView, DeleteView',
            'from django_filters.views import FilterView',
            'from django.urls import reverse_lazy',
            f'from .models import {model_name}',
            f'from .forms import {model_name}Form',
            f'from .tables import {model_name}Table',
            f'from .filters import {model_name}Filter'
        ]
        for import_statement in imports:
            add_import_if_missing(views_file, import_statement)

        # Construct the views content
        views_content = [
            "",
            f"class {model_name}ListView(PageHeaderMixin, CustomSingleTableMixin, FilterView):",
            f"    model = {model_name}",
            f"    table_class = {model_name}Table",
            f"    template_name = 'list.html'",
            f"    filterset_class = {model_name}Filter",
            f"    #ordering = ['some_field']",
            f"    page_title = 'All {model_name}s'",
            f"    add_link = reverse_lazy('{model_name.lower()}_add')",
            f"    add_perms = '{model_name.lower()}.add_{model_name.lower()}'",
            f"    edit_perms = '{model_name.lower()}.change_{model_name.lower()}'",
            f"    delete_perms = '{model_name.lower()}.delete_{model_name.lower()}'",
            "",
            f"class {model_name}CreateView(LoginRequiredMixin, PageHeaderMixin, CreateView):",
            f"    model = {model_name}",
            f"    form_class = {model_name}Form",
            f"    template_name = 'add.html'",
            f"    success_url = reverse_lazy('{model_name.lower()}_list')",
            f"    page_title = '{model_name}'",
            f"    list_link = reverse_lazy('{model_name.lower()}_list')",
            "",
            f"class {model_name}UpdateView(LoginRequiredMixin, PageHeaderMixin, UpdateView):",
            f"    model = {model_name}",
            f"    form_class = {model_name}Form",
            f"    template_name = 'add.html'",
            f"    success_url = reverse_lazy('{model_name.lower()}_list')",
            f"    page_title = 'Update {model_name}'",
            f"    list_link = reverse_lazy('{model_name.lower()}_list')",
            "",
            f"class {model_name}DeleteView(LoginRequiredMixin, PageHeaderMixin, DeleteView):",
            f"    model = {model_name}",
            f"    template_name = 'delete.html'",
            f"    page_title = 'Delete {model_name}'",
            f"    success_url = reverse_lazy('{model_name.lower()}_list')",
        ]

        # Write the views content to the file
        with open(views_file, 'a') as file:
            file.write("\n".join(views_content) + "\n")


    def generate_forms(self, model):
        model_name = model.__name__
        forms_file = "apps/ecom/forms.py"

        # Add imports if missing
        imports = [
            'from django import forms',
            'from crispy_forms.helper import FormHelper',
            'from crispy_forms.layout import Layout, Row, Column, HTML, Submit',
            f'from .models import {model_name}'
        ]
        for import_statement in imports:
            add_import_if_missing(forms_file, import_statement)

        # Create fields list for the form dynamically
        fields = ", ".join([f"'{field.name}'" for field in model._meta.fields if field.name != 'id'])
        form_fields = ", ".join([f"'{field.name}'" for field in model._meta.fields if field.name != 'id'])

        # Prepare the form content with proper alignment
        forms_content = [
        "",
        f"class {model_name}Form(forms.ModelForm):",
        "    class Meta:",
        f"        model = {model_name}",
        f"        fields = ({fields},)",
        "",
        "    def __init__(self, *args, **kwargs):",
        "        super().__init__(*args, **kwargs)",
        "        self.helper = FormHelper()",
        "        self.helper.layout = Layout(",
        "            Row(",
        f"                Column({form_fields}),",
        "            ),",
        "            Row(",
        "                Column(",
        "                   Submit('submit', 'Save', css_class='btn btn-primary', "
        "              onclick=\"return confirm('Are you sure you want to submit?');\")",
        "                ),",
        "            )",
        "        )",
        "",
        f"class {model_name}FilterForm(forms.Form):",
        "    def __init__(self, *args, **kwargs):",
        "        super().__init__(*args, **kwargs)",
        "        self.helper = FormHelper()",
        "        self.helper.form_method = 'get'",
        "        self.helper.layout = Layout(",
        "            Row(",
        "".join([f"                Column('{field.name}', css_class='form-group col-md-4 mb-0'),\n" for field in model._meta.fields if field.name != 'id']),
        "                Column(HTML(\"\"\"<button class='btn btn-lg btn-primary'>Filter</button>\"\"\"),",
        "                       css_class='form-group col-md-2 p-5 mb-0'),",
        "            ),",
        "        )",
    ]


        # Write the content to the forms file, ensuring proper alignment
        with open(forms_file, 'a') as file:
            file.write("\n".join(forms_content) + "\n")



    def generate_filters(self, model):
        model_name = model.__name__
        filters_file = "apps/ecom/filters.py"

        # Add imports if missing
        imports = [
            'import django_filters',
            f'from .models import {model_name}',
            f'from .forms import {model_name}FilterForm'
        ]
        for import_statement in imports:
            add_import_if_missing(filters_file, import_statement)

        # Create the filter fields dynamically
        fields = ", ".join([f"'{field.name}'" for field in model._meta.fields if field.name != 'id'])

        # Prepare the filter content with proper alignment
        filters_content = [
            "",
            f"class {model_name}Filter(django_filters.FilterSet):",
            "    class Meta:",
            f"        model = {model_name}",
            f"        fields = [{fields}]",
            f"        form = {model_name}FilterForm"
        ]

        # Write the content to the filters file, ensuring it's properly aligned
        with open(filters_file, 'a') as file:
            file.write("\n".join(filters_content) + "\n")


    def generate_tables(self, model):
        model_name = model.__name__
        tables_file = "apps/ecom/tables.py"

        # Add imports if missing
        add_import_if_missing(tables_file, 'import django_tables2 as tables')
        add_import_if_missing(tables_file, 'from apps.helpers import CustomTable')  # Assuming CustomTable is your custom class
        add_import_if_missing(tables_file, f'from .models import {model_name}')

        # Generate fields list dynamically, excluding 'id' and 'selected'
        fields = ", ".join([f"'{field.name}'" for field in model._meta.fields if field.name not in ['id', 'selected']])

        tables_content = [
            "",
            f"class {model_name}Table(CustomTable):",
            f"    edit_url = '{model_name.lower()}_update'",
            f"    delete_url = '{model_name.lower()}_delete'",
            f"    class Meta:",
            f"        model = {model_name}",
            f"        template_name = 'django_tables2/bootstrap4.html'",
            f"        fields = [{fields}]",
            f"        empty_text = 'No {model_name.lower()}s available'",
            f"        orderable = True",
            f"        exclude = ('selected',)",
        ]

        # Append the content to tables.py
        with open(tables_file, 'a') as file:
            file.write('\n'.join(tables_content))


        
    def generate_urls(self, model):
        print("generating urls")
        model_name = model.__name__.lower()
        views_imports = f"from .views import {model.__name__}CreateView, {model.__name__}DeleteView, {model.__name__}ListView, {model.__name__}UpdateView"
        urls_file = "apps/ecom/urls.py"

        # Read the current content of urls.py
        with open(urls_file, 'r') as file:
            content = file.readlines()

        # Check if the necessary import already exists and add it at the top if it's missing
        if views_imports not in "".join(content):
            # Find the first non-import line to insert the imports at the correct location
            for index, line in enumerate(content):
                if not line.startswith("from") and not line.startswith("import"):
                    content.insert(index, views_imports + "\n")
                    break

        # Prepare the URL patterns for the model
        url_patterns = [
            f"    path('{model_name}/', {model.__name__}ListView.as_view(), name='{model_name}_list'),",
            f"    path('{model_name}/add/', {model.__name__}CreateView.as_view(), name='{model_name}_add'),",
            f"    path('{model_name}/<int:pk>/update/', {model.__name__}UpdateView.as_view(), name='{model_name}_update'),",
            f"    path('{model_name}/<int:pk>/delete/', {model.__name__}DeleteView.as_view(), name='{model_name}_delete'),"
        ]

        # Look for the `urlpatterns` list and insert the new URL patterns right before the last closing bracket
        for index, line in enumerate(content):
            if 'urlpatterns' in line:
                # Insert URL patterns before the closing bracket
                for pattern in url_patterns:
                    if pattern.strip() not in "".join(content):  # Avoid adding duplicates
                        content.insert(index + 1, f"{pattern}\n")

        # Write the updated content back to urls.py
        with open(urls_file, 'w') as file:
            file.writelines(content)
