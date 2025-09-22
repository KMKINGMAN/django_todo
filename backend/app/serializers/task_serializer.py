"""
    Task Serializers for the Todo application.
"""
from rest_framework import serializers
from ..models import Task, Todo


class TaskTodoSerializer(serializers.ModelSerializer):
    """Simplified serializer for todos within tasks to avoid circular imports."""

    class Meta:
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

    class Meta:
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
        """Get todos for this task filtered by current user.

        Skip querying/serializing todos when serializer context indicates the
        client did not request them (include_todos=False). The view is
        responsible for placing `include_todos` into the serializer context.
        """
        include = self.context.get('include_todos', False)
        if not include:
            return []

        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            todos_queryset = obj.todos.filter(
                user=request.user).order_by('-created_at')
            return TaskTodoSerializer(todos_queryset, many=True).data
        return []

    def get_todos_count(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
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
                    todo = Todo.objects.get(
                        id=todo_id, user=self.context['request'].user)
                    for field, value in todo_data.items():
                        if field != 'id':
                            setattr(todo, field, value)
                    todo.save()
                    if todo not in instance.todos.all():
                        instance.todos.add(todo)
                except Todo.DoesNotExist:
                    # Skip if todo doesn't exist or doesn't belong to user
                    continue
            else:
                # Create new todo
                todo = Todo.objects.create(
                    **{k: v for k, v in todo_data.items() if k != 'id'})
                todo.user.add(self.context['request'].user)
                instance.todos.add(todo)

        return instance
