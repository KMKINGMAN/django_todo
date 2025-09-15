"""
    Todo Serializers for the Todo application.
"""
from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import Todo


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