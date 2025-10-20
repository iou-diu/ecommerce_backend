from django.urls import path
from . import views

urlpatterns = [
    path('generate-hotspot/', views.HotspotAddView.as_view(), name='generate_hotspot'),

    path('create-hotspot-api/', views.create_hotspot_api, name='create_hotspot_api'),
    path('get_products/', views.get_products, name='get_products'),
]
