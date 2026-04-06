from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from apps.cms.models import HomeSlider, Catalog, CorporateLead, CorporateLeadActivity

class HomeSliderForm(forms.ModelForm):
    class Meta:
        model = HomeSlider
        fields = ['type', 'title', 'description', 'image', 'button_title', 'button_link', 'order']
        widgets = {
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'button_title': forms.TextInput(attrs={'class': 'form-control'}),
            'button_link': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('type', css_class='form-group col-md-4 mb-0'),
                Column('title', css_class='form-group col-md-8 mb-0'),
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('image', css_class='form-group col-md-6 mb-0'),
                Column('button_title', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('button_link', css_class='form-group col-md-9 mb-0'),
                Column('order', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save Slider', css_class='btn btn-primary btn-lg px-10'),
                    css_class='form-group col-md-12 text-center mt-5'
                ),
            ),
        )

class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = (
            'tagline', 'title', 'slug', 'description', 
            'banner_image', 'thumbnail_image', 
            'is_published', 'is_featured', 
            'published_date', 'meta_description'
        )
        widgets = {
            'tagline': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'banner_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'thumbnail_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'published_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6 mb-0'),
                Column('slug', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('tagline', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('banner_image', css_class='form-group col-md-6 mb-0'),
                Column('thumbnail_image', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('published_date', css_class='form-group col-md-4 mb-0'),
                Column('is_published', css_class='form-group col-md-4 mb-0 p-10'),
                Column('is_featured', css_class='form-group col-md-4 mb-0 p-10'),
            ),
            Row(
                Column('meta_description', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save Catalog', css_class='btn btn-primary btn-lg px-10'),
                    css_class='form-group col-md-12 text-center mt-5'
                ),
            ),
        )

class CatalogFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-4 mb-0'),
                Column('is_published', css_class='form-group col-md-2 mb-0'),
                Column('is_featured', css_class='form-group col-md-2 mb-0'),
                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )

class CorporateLeadForm(forms.ModelForm):
    class Meta:
        model = CorporateLead
        fields = ['status', 'priority', 'assigned_to', 'project_details']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control select2'}),
            'project_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('status', css_class='form-group col-md-6 mb-0'),
                Column('priority', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('assigned_to', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('project_details', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column(
                    Submit('submit', 'Update Lead', css_class='btn btn-primary btn-lg px-10'),
                    css_class='form-group col-md-12 text-center mt-5'
                ),
            ),
        )


class CorporateLeadActivityForm(forms.ModelForm):
    class Meta:
        model = CorporateLeadActivity
        fields = ['activity_type', 'description', 'followup_date']
        widgets = {
            'activity_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write notes or interaction details...'}),
            'followup_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('activity_type', css_class='form-group col-md-6'),
                Column('followup_date', css_class='form-group col-md-6'),
            ),
            Row(
                Column('description', css_class='form-group col-md-12'),
            ),
            Row(
                Column(
                    Submit('submit_activity', 'Add Note', css_class='btn btn-success btn-block'),
                    css_class='col-md-12'
                ),
            ),
        )


class CorporateLeadFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('company_name', css_class='form-group col-md-4 mb-0'),
                Column('status', css_class='form-group col-md-4 mb-0'),
                Column(HTML("""<button class='btn btn-lg btn-primary mt-6'>Filter</button>"""),
                       css_class='form-group col-md-4 mb-0'),
            ),
        )
class NewsLetterFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-8 mb-0'),
                Column(HTML("""<button class='btn btn-lg btn-primary mt-6'>Filter</button>"""),
                       css_class='form-group col-md-4 mb-0'),
            ),
        )
