"""
Django admin configuration for Todo application.

This module defines the admin interface for managing Todo instances.
"""

from django.contrib import admin

from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    """Admin interface for Todo model."""
    
    list_display = (
        'id', 'title', 'completed', 'due_date', 
        'created_at', 'updated_at', 'tags', 'description'
    )
    list_filter = (
        'completed', 'tags', 'user', 'created_at', 'updated_at'
    )
    search_fields = ('title', 'description', 'tags')
    list_editable = ('completed',)
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'completed')
        }),
        ('Timing', {
            'fields': ('due_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Organization', {
            'fields': ('tags', 'user')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('user',)
