"""
Django app configuration for the app module.

This module contains the Django application configuration for the todo app.
"""

from django.apps import AppConfig


class TodoAppConfig(AppConfig):
    """Configuration for the Todo application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
