from django.urls import path
from . import views
 
urlpatterns = [
    path('home-slider/', views.HomeSliderView.as_view(), name='home_slider'),
    path('home-slider/create/', views.HomeSliderCreateView.as_view(), name='home_slider_create'),
    path('home-slider/update/<int:pk>/', views.HomeSliderUpdateView.as_view(), name='home_slider_update'),
    path('home-slider/delete/<int:pk>/', views.HomeSliderDeleteView.as_view(), name='home_slider_delete'),
    path('contacts/', views.ContactFormListView.as_view(), name='contact_list'),
    path('contacts/ajax/', views.contact_form_ajax, name='contact_list_ajax'),

    # Catalog URLs
    path('catalog/', views.CatalogListView.as_view(), name='catalog_list'),
    path('catalog/create/', views.CatalogCreateView.as_view(), name='catalog_create'),
    path('catalog/update/<int:pk>/', views.CatalogUpdateView.as_view(), name='catalog_update'),
    path('catalog/delete/<int:pk>/', views.CatalogDeleteView.as_view(), name='catalog_delete'),
    path('catalog/detail/<int:pk>/', views.CatalogDetailView.as_view(), name='catalog_detail'),

    # Corporate Lead URLs
    path('leads/', views.CorporateLeadListView.as_view(), name='corporate_lead_list'),
    path('leads/detail/<int:pk>/', views.CorporateLeadDetailView.as_view(), name='corporate_lead_detail'),
    path('leads/delete/<int:pk>/', views.CorporateLeadDeleteView.as_view(), name='corporate_lead_delete'),
    
    # NewsLetter URLs
    path('newsletter/', views.NewsLetterListView.as_view(), name='newsletter_list'),
    path('newsletter/delete/<int:pk>/', views.NewsLetterDeleteView.as_view(), name='newsletter_delete'),
]
