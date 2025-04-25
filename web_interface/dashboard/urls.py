from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('visualizations/', views.visualizations, name='visualizations'),
    path('data/', views.data_view, name='data_view'),
]