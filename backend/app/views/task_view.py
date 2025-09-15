
"""
Todo application views.

This module contains Django REST Framework views and serializers for the Todo model.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Todo, Task
from ..serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Task instances via REST API."""
    
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return tasks filtered by current user or all for superuser."""
        if self.request.user.is_superuser:
            return Task.objects.all().order_by('-created_at')
        return Task.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """Associate created task with current user."""
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        """Delete task and all related todos owned by the user."""
        # Get todos that belong to this task and this user
        user_todos = instance.todos.filter(user=self.request.user)
        
        # If user is superuser, delete all todos in this task
        if self.request.user.is_superuser:
            user_todos = instance.todos.all()
            
        # Delete the todos
        for todo in user_todos:
            todo.delete()
            
        # Delete the task
        instance.delete()


