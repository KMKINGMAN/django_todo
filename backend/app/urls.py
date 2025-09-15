"""
URL configuration for Todo app.

This module defines the API endpoints for the Todo application using
Django REST Framework routers and URL patterns.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TodoViewSet, TaskViewSet


# Create router and register viewsets
router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')
router.register(r'tasks', TaskViewSet, basename='task')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
