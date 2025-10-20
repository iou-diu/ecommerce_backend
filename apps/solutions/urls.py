from django.urls import path
from . import views

urlpatterns = [
    path('', views.solution_list, name='solution_list'),
    path('add/', views.solution_add, name='solution_add'),
    path('<int:pk>/edit/', views.solution_edit, name='solution_edit'),
]
