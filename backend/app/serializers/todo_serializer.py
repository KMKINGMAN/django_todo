"""
    Todo Serializers for the Todo application.
"""
from rest_framework import serializers
from ..models import Todo, Task


class TodoSerializer(serializers.ModelSerializer):
    """Serializer for Todo model with user association and tags support."""
    user = serializers.StringRelatedField(read_only=True)
    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        required=False,
        allow_null=True
    )
    task_title = serializers.CharField(source='task.title', read_only=True)
    tags = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

    class Meta:
        """Meta configuration for TodoSerializer."""
        model = Todo
        fields = [
            'id', 'title', 'completed', 'created_at', 'description',
            'due_date', 'updated_at', 'user', 'task', 'task_title', 'tags'
        ]
        read_only_fields = ['created_at', 'updated_at', 'user']

    def create(self, validated_data):
        """Create a new Todo instance with proper user and tags handling."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
