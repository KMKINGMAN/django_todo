
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


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def todo_function_view(request: Request):
    """
    Function-based view for todo operations.
    
    Note: This is kept for compatibility but TodoViewSet is preferred.
    """
    if request.method == 'GET':
        todos = Todo.objects.filter(
            user=request.user
        ).order_by('-created_at')
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            todo_instance = serializer.save()
            todo_instance.user.add(request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        
    elif request.method == 'PATCH':
        todo_id = request.data.get('id')
        if not todo_id:
            return Response(
                {'error': 'ID is required for PATCH'}, 
                status=400
            )
            
        try:
            todo_instance = Todo.objects.get(id=todo_id)
        except Todo.DoesNotExist:
            return Response(
                {'error': 'Todo not found'}, 
                status=404
            )
            
        serializer = TodoSerializer(
            todo_instance, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
        
    elif request.method == 'DELETE':
        todo_id = request.data.get('id')
        if not todo_id:
            return Response(
                {'error': 'ID is required for DELETE'}, 
                status=400
            )
            
        try:
            todo_instance = Todo.objects.get(id=todo_id)
        except Todo.DoesNotExist:
            return Response(
                {'error': 'Todo not found'}, 
                status=404
            )
            
        todo_instance.delete()
        return Response(status=204)


@login_required
def dashboard(request):
    """Render the dashboard template for authenticated users."""
    return render(request, 'dashboard.html', {'user': request.user})
