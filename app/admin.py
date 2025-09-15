"""
Django admin configuration for Todo application.

This module defines the admin interface for managing Todo and Task instances.
"""

from django.contrib import admin

from .models import Todo, Task


class TodoInline(admin.TabularInline):
    """Inline admin for managing todos within a task."""
    model = Task.todos.through
    extra = 1
    verbose_name = "Todo"
    verbose_name_plural = "Todos"


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


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin interface for Task model with inline todo editing."""
    
    list_display = (
        'id', 'title', 'user', 'created_at', 'updated_at', 'todos_count'
    )
    list_filter = ('user', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'user__username')
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'user')
        }),
        ('Timing', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    inlines = [TodoInline]
    filter_horizontal = ('todos',)

    def todos_count(self, obj):
        """Return the number of todos in this task."""
        return obj.todos.count()
    todos_count.short_description = 'Todos Count'

    def get_queryset(self, request):
        """Filter tasks based on user permissions."""
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit user selection to current user for non-superusers."""
        if db_field.name == "user" and not request.user.is_superuser:
            kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """Ensure user is set to current user if not specified."""
        if not obj.user_id and not request.user.is_superuser:
            obj.user = request.user
        super().save_model(request, obj, form, change)
