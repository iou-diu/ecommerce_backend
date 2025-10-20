from django.urls import path
from . import views

urlpatterns = [
    path('aidashboard/', views.ai_dashboard, name='ai_dashboard'),
]
