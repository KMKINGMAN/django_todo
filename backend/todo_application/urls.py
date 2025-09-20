"""
URL configuration for todo_application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path

from app import views as app_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', app_views.dashboard, name='dashboard'),
]
