"""
    Task Serializers for the Todo application.
"""
from rest_framework import serializers
from ..models import Task, Todo


class TaskTodoSerializer(serializers.ModelSerializer):
    """Simplified serializer for todos within tasks to avoid circular imports."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta configuration for TaskTodoSerializer."""
        model = Todo
        fields = [
            'id',
            'title',
            'description',
            'completed',
            'created_at',
            'updated_at',
            'tags',
            'due_date']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model with nested todos support."""
    todos = serializers.SerializerMethodField()
    todos_count = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True)

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta configuration for TaskSerializer."""
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'updated_at',
            'user',
            'todos',
            'todos_count']
        read_only_fields = ['created_at', 'updated_at', 'user']

    def get_todos(self, obj):
        """Get todos for this task filtered by current user."""
        request = self.context.get('request')
        if request and hasattr(request,
                               'user') and request.user.is_authenticated:
            # Get todos that belong to this task and current user
            todos_queryset = obj.todos.filter(
                user=request.user).order_by('-created_at')
            return TaskTodoSerializer(todos_queryset, many=True).data
        return []

    def get_todos_count(self, obj):
        """Get the count of todos for this task filtered by current user."""
        request = self.context.get('request')
        if request and hasattr(request,
                               'user') and request.user.is_authenticated:
            return obj.todos.filter(user=request.user).count()
        return 0

    def create(self, validated_data):
        """Create a new Task instance."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update Task instance and replace its todos."""
        todos_data = validated_data.pop('todos', [])

        # Update task fields
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()

        # Handle todos - either update existing or create new ones
        for todo_data in todos_data:
            todo_id = todo_data.get('id')
            if todo_id:
                # Update existing todo
                try:
                    todo = Todo.objects.get(  # pylint: disable=no-member
                        id=todo_id, user=self.context['request'].user)
                    for field, value in todo_data.items():
                        if field != 'id':
                            setattr(todo, field, value)
                    todo.save()
                    if todo not in instance.todos.all():
                        instance.todos.add(todo)
                except Todo.DoesNotExist:  # pylint: disable=no-member
                    # Skip if todo doesn't exist or doesn't belong to user
                    continue
            else:
                # Create new todo
                todo = Todo.objects.create(  # pylint: disable=no-member
                    **{k: v for k, v in todo_data.items() if k != 'id'})
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
