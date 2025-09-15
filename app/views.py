
"""
Todo application views.

This module contains Django REST Framework views and serializers for the Todo model.
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    """Serializer for Todo model with user association and tags support."""
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        many=True, 
        required=False
    )
    tags = serializers.ListField(
        child=serializers.CharField(), 
        required=False
    )

    class Meta:
        model = Todo
        fields = [
            'id', 'title', 'completed', 'created_at', 'description', 
            'due_date', 'updated_at', 'user', 'tags'
        ]

    def create(self, validated_data):
        """Create a new Todo instance with proper user and tags handling."""
        users = validated_data.pop('user', [])
        tags = validated_data.pop('tags', None)
        todo = Todo.objects.create(**validated_data)
        
        if users:
            todo.user.set(users)
        if tags is not None:
            todo.tags = tags
            todo.save()
            
        return todo


class TodoViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Todo instances via REST API."""
    
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return todos filtered by current user."""
        return Todo.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

    def perform_create(self, serializer):
        """Associate created todo with current user."""
        todo = serializer.save()
        todo.user.add(self.request.user)

@login_required
def dashboard(request):
    """Render the dashboard template for authenticated users."""
    return render(request, 'dashboard.html', {'user': request.user})
