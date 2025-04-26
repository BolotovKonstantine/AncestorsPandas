from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('visualizations/', views.visualizations, name='visualizations'),
    path('data/', views.data_view, name='data_view'),
    path('data-sources/', views.data_sources, name='data_sources'),
    path('data-sources/create/', views.data_source_create, name='data_source_create'),
    path('data-sources/<int:pk>/edit/', views.data_source_edit, name='data_source_edit'),
    path('data-sources/<int:pk>/delete/', views.data_source_delete, name='data_source_delete'),
    path('data-sources/preview/', views.data_source_preview, name='data_source_preview'),
    path('data-sources/<int:pk>/normalize/', views.data_source_normalize, name='data_source_normalize'),
]
