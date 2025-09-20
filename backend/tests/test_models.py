"""
Model tests for Todo and Task models.

This module contains unit tests for the Todo and Task models
including validation, relationships, and model methods.

"""

import pytest
from django.contrib.auth.models import User
from app.models import Todo, Task


@pytest.mark.django_db
class TestTodoModel:
    """Test cases for the Todo model."""

    def test_create_todo_minimal(self):
        """Test creating a todo with minimal required fields."""
        user = User.objects.create_user(username="testuser", password="pass123")

        todo = Todo.objects.create(title="Test Todo", user=user)

        assert todo.title == "Test Todo"
        assert todo.user == user
        assert todo.completed is False
        assert todo.description is None
        assert todo.task is None
        assert todo.tags == ["general"]  # Default tags
        assert todo.created_at is not None
        assert todo.updated_at is not None

    def test_create_todo_full_fields(self):
        """Test creating a todo with all fields populated."""
        user = User.objects.create_user(username="testuser", password="pass123")
        task = Task.objects.create(title="Test Task", user=user)

        todo = Todo.objects.create(
            title="Full Todo",
            description="Full description",
            completed=True,
            user=user,
            task=task,
            tags=["work", "important"],
        )

        assert todo.title == "Full Todo"
        assert todo.description == "Full description"
        assert todo.completed is True
        assert todo.user == user
        assert todo.task == task
        assert todo.tags == ["work", "important"]

    def test_todo_str_representation(self):
        """Test the string representation of Todo model."""
        user = User.objects.create_user(username="testuser", password="pass123")

        # Test normal title
        todo = Todo.objects.create(title="Short Title", user=user)
        assert str(todo) == "Short Title"

        # Test long title (should be truncated)
        long_title = "A" * 60  # 60 characters
        todo_long = Todo.objects.create(title=long_title, user=user)
        assert str(todo_long) == f"{long_title[:50]}..."

    def test_todo_repr_representation(self):
        """Test the repr representation of Todo model."""
        user = User.objects.create_user(username="testuser", password="pass123")
        todo = Todo.objects.create(title="Test Todo", user=user)

        expected_repr = f"Todo(id={todo.id}, title='Test Todo', completed=False, user=testuser)"
        assert repr(todo) == expected_repr

    def test_todo_ordering(self):
        """Test that todos are ordered by creation date (newest first)."""
        user = User.objects.create_user(username="testuser", password="pass123")

        todo1 = Todo.objects.create(title="First", user=user)
        todo2 = Todo.objects.create(title="Second", user=user)
        todo3 = Todo.objects.create(title="Third", user=user)

        todos = list(Todo.objects.all())
        assert todos[0] == todo3  # Newest first
        assert todos[1] == todo2
        assert todos[2] == todo1

    def test_todo_user_relationship(self):
        """Test the foreign key relationship with User."""
        user = User.objects.create_user(username="testuser", password="pass123")

        todo1 = Todo.objects.create(title="Todo 1", user=user)
        todo2 = Todo.objects.create(title="Todo 2", user=user)

        # Test reverse relationship
        user_todos = user.todos.all()
        assert todo1 in user_todos
        assert todo2 in user_todos
        assert len(user_todos) == 2

    def test_todo_task_relationship(self):
        """Test the foreign key relationship with Task."""
        user = User.objects.create_user(username="testuser", password="pass123")
        task = Task.objects.create(title="Test Task", user=user)

        todo1 = Todo.objects.create(title="Todo 1", task=task, user=user)
        todo2 = Todo.objects.create(title="Todo 2", task=task, user=user)

        # Test reverse relationship
        task_todos = task.todos.all()
        assert todo1 in task_todos
        assert todo2 in task_todos
        assert len(task_todos) == 2

    def test_todo_without_task(self):
        """Test creating a todo without associating it with a task."""
        user = User.objects.create_user(username="testuser", password="pass123")

        todo = Todo.objects.create(title="Standalone Todo", user=user)

        assert todo.task is None

    def test_todo_cascade_delete_user(self):
        """Test that todos are deleted when user is deleted."""
        user = User.objects.create_user(username="testuser", password="pass123")
        todo = Todo.objects.create(title="Test Todo", user=user)

        user.delete()

        # Todo is deleted due to CASCADE relationship
        assert not Todo.objects.filter(id=todo.id).exists()

    def test_todo_cascade_delete_task(self):
        """Test that todos are deleted when associated task is deleted."""
        user = User.objects.create_user(username="testuser", password="pass123")
        task = Task.objects.create(title="Test Task", user=user)
        todo = Todo.objects.create(title="Test Todo", task=task, user=user)

        task.delete()

        # Todo is deleted due to CASCADE relationship
        assert not Todo.objects.filter(id=todo.id).exists()


@pytest.mark.django_db
@pytest.mark.unit
class TestTaskModel:
    """Test cases for the Task model."""

    def test_create_task_minimal(self):
        """Test creating a task with minimal required fields."""
        user = User.objects.create_user(username="testuser", password="pass123")

        task = Task.objects.create(title="Test Task", user=user)

        assert task.title == "Test Task"
        assert task.user == user
        assert task.description is None
        assert task.created_at is not None
        assert task.updated_at is not None

    def test_create_task_full_fields(self):
        """Test creating a task with all fields populated."""
        user = User.objects.create_user(username="testuser", password="pass123")

        task = Task.objects.create(
            title="Full Task", description="Full description", user=user
        )

        assert task.title == "Full Task"
        assert task.description == "Full description"
        assert task.user == user

    def test_task_str_representation(self):
        """Test the string representation of Task model."""
        user = User.objects.create_user(username="testuser", password="pass123")

        # Test normal title
        task = Task.objects.create(title="Short Title", user=user)
        assert str(task) == "Short Title"

        # Test long title (should be truncated)
        long_title = "B" * 60  # 60 characters
        task_long = Task.objects.create(title=long_title, user=user)
        assert str(task_long) == f"{long_title[:50]}..."

    def test_task_repr_representation(self):
        """Test the repr representation of Task model."""
        user = User.objects.create_user(username="testuser", password="pass123")
        task = Task.objects.create(title="Test Task", user=user)

        expected_repr = f"Task(id={task.id}, title='Test Task', user={user.username})"
        assert repr(task) == expected_repr

    def test_task_ordering(self):
        """Test that tasks are ordered by creation date (newest first)."""
        user = User.objects.create_user(username="testuser", password="pass123")

        task1 = Task.objects.create(title="First", user=user)
        task2 = Task.objects.create(title="Second", user=user)
        task3 = Task.objects.create(title="Third", user=user)

        tasks = list(Task.objects.all())
        assert tasks[0] == task3  # Newest first
        assert tasks[1] == task2
        assert tasks[2] == task1

    def test_task_user_relationship(self):
        """Test the foreign key relationship with User."""
        user = User.objects.create_user(username="testuser", password="pass123")

        task1 = Task.objects.create(title="Task 1", user=user)
        task2 = Task.objects.create(title="Task 2", user=user)

        # Test reverse relationship
        user_tasks = user.tasks.all()
        assert task1 in user_tasks
        assert task2 in user_tasks
        assert len(user_tasks) == 2

    def test_task_cascade_delete_user(self):
        """Test that tasks are deleted when user is deleted."""
        user = User.objects.create_user(username="testuser", password="pass123")
        task = Task.objects.create(title="Test Task", user=user)

        user.delete()

        # Task should be deleted due to CASCADE
        assert not Task.objects.filter(id=task.id).exists()

    def test_task_with_todos_relationship(self):
        """Test the relationship between task and its todos."""
        user = User.objects.create_user(username="testuser", password="pass123")
        task = Task.objects.create(title="Parent Task", user=user)

        # Create todos associated with the task
        todo1 = Todo.objects.create(title="Todo 1", task=task, user=user)
        todo2 = Todo.objects.create(title="Todo 2", task=task, user=user)

        # Test that task can access its todos
        task_todos = task.todos.all()
        assert len(task_todos) == 2
        assert todo1 in task_todos
        assert todo2 in task_todos
