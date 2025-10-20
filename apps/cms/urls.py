from django.urls import path
from . import views

urlpatterns = [
    path('home-slider/', views.HomeSliderView.as_view(), name='home_slider'),
    path('contacts/', views.ContactFormListView.as_view(), name='contact_list'),
    path('contacts/ajax/', views.contact_form_ajax, name='contact_list_ajax'),
]
