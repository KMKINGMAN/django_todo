"""
    Task Serializers for the Todo application.
"""
from rest_framework import serializers
from .todo_serializer import TodoSerializer
from ..models import Task, Todo

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model with nested todos support."""
    todos = TodoSerializer(many=True, required=False)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'user', 'todos']
        read_only_fields = ['created_at', 'updated_at', 'user']

    def create(self, validated_data):
        """Create a new Task instance with nested todos."""
        todos_data = validated_data.pop('todos', [])
        task = Task.objects.create(**validated_data)
        
        for todo_data in todos_data:
            todo = Todo.objects.create(**todo_data)
            todo.user.add(self.context['request'].user)
            task.todos.add(todo)
            
        return task

    def update(self, instance, validated_data):
        """Update Task instance and replace its todos."""
        todos_data = validated_data.pop('todos', [])
        
        # Update task fields
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        
        # Handle todos - either update existing or create new ones
        for todo_data in todos_data:
            todo_id = todo_data.get('id')
            if todo_id:
                # Update existing todo
                try:
                    todo = Todo.objects.get(id=todo_id, user=self.context['request'].user)
                    for field, value in todo_data.items():
                        if field != 'id':
                            setattr(todo, field, value)
                    todo.save()
                    if todo not in instance.todos.all():
                        instance.todos.add(todo)
                except Todo.DoesNotExist:
                    # Todo doesn't exist or doesn't belong to user
                    continue
            else:
                # Create new todo
                todo = Todo.objects.create(**{k: v for k, v in todo_data.items() if k != 'id'})
                todo.user.add(self.context['request'].user)
                instance.todos.add(todo)
        
        return instance

    def to_representation(self, instance):
        """Customize representation based on include_todos parameter."""
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        if request and request.query_params.get('include_todos') != '1':
            data.pop('todos', None)
            
        return data
