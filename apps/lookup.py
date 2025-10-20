from django_select2.forms import ModelSelect2Widget
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget
from django import forms


class CustomSelect2Mixin(ModelSelect2Widget):
    @property
    def media(self):
        return forms.Media([])


class CustomSelect2MultipleMixin(ModelSelect2MultipleWidget):
    @property
    def media(self):
        return forms.Media([])