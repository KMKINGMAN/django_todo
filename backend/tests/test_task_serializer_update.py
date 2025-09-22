"""Unit tests for TaskSerializer.update behavior."""

import pytest
from django.contrib.auth.models import User

from app.models import Task, Todo
from app.serializers.task_serializer import TaskSerializer

pytestmark = pytest.mark.django_db


def test_task_serializer_update_updates_and_creates_todos():
    # Create user and initial task+todo
    user = User.objects.create_user(username="tester", password="pass")
    task = Task.objects.create(title="Initial Task", description="desc", user=user)
    existing_todo = Todo.objects.create(title="Existing", user=user, task=task)

    # Prepare serializer with request context containing the user
    # Build serializer context similar to view (request with user)
    context = {"request": type("R", (), {"user": user})()}

    # Data: update existing todo title, and add a new todo
    payload = {
        "title": "Updated Task Title",
        "description": "Updated",
        "todos": [
            {"id": existing_todo.id, "title": "Existing - Updated"},
            {"title": "New Todo", "description": "new desc"},
        ],
    }

    # We want to exercise the serializer.update() implementation directly.
    serializer = TaskSerializer(
        instance=task, data=payload, partial=True, context=context
    )
    assert serializer.is_valid(), serializer.errors
    validated = dict(serializer.validated_data)
    validated["todos"] = payload["todos"]
    _updated = serializer.update(task, validated)

    # Refresh from DB
    existing_todo.refresh_from_db()
    assert existing_todo.title == "Existing - Updated"
    # Ensure the existing todo still points to the same task and user
    assert existing_todo.task_id == task.id
    assert existing_todo.user_id == user.id

    # New todo should have been created and assigned
    new_todos = Todo.objects.filter(title="New Todo", user=user, task=task)
    assert new_todos.exists()

    # Task fields updated
    task.refresh_from_db()
    assert task.title == "Updated Task Title"


def test_task_serializer_update_reassigns_existing_todo_from_other_task():
    """If a user provides an existing todo that belongs to a different task
    but is still owned by the user, the update() should reassign it to the
    target task."""
    user = User.objects.create_user(username="owner", password="pw")
    original_task = Task.objects.create(title="Original", user=user)
    target_task = Task.objects.create(title="Target", user=user)
    todo = Todo.objects.create(title="MoveMe", user=user, task=original_task)

    context = {"request": type("R", (), {"user": user})()}
    payload = {"todos": [{"id": todo.id, "title": "MoveMe - updated"}]}

    serializer = TaskSerializer(
        instance=target_task, data=payload, partial=True, context=context
    )
    assert serializer.is_valid(), serializer.errors
    validated = dict(serializer.validated_data)
    validated["todos"] = payload["todos"]
    _updated_reassign = serializer.update(target_task, validated)

    todo.refresh_from_db()
    assert todo.task_id == target_task.id
    assert todo.title == "MoveMe - updated"


def test_task_serializer_update_skips_todo_owned_by_other_user():
    """If a provided todo id exists but belongs to another user, it should
    be skipped and not raised as an error."""
    user1 = User.objects.create_user(username="u1", password="pw")
    user2 = User.objects.create_user(username="u2", password="pw")
    task = Task.objects.create(title="Task", user=user1)
    other_task = Task.objects.create(title="Other", user=user2)
    other_todo = Todo.objects.create(title="TheirTodo", user=user2, task=other_task)

    context = {"request": type("R", (), {"user": user1})()}
    payload = {"todos": [{"id": other_todo.id, "title": "Attempted Update"}]}

    serializer = TaskSerializer(
        instance=task, data=payload, partial=True, context=context
    )
    assert serializer.is_valid(), serializer.errors
    validated = dict(serializer.validated_data)
    validated["todos"] = payload["todos"]
    _updated_skipped = serializer.update(task, validated)
    other_todo.refresh_from_db()
    assert other_todo.title == "TheirTodo"


def test_get_todos_and_count_with_unauthenticated_request():
    """Ensure serializer returns empty todos and zero count for anonymous users."""
    user = User.objects.create_user(username="authuser", password="pw")
    task = Task.objects.create(title="TaskAuth", user=user)
    Todo.objects.create(title="T1", user=user, task=task)

    # Anonymous request (no authenticated user)
    context = {
        "request": type(
            "R", (), {"user": type("Anon", (), {"is_authenticated": False})()}
        )()
    }
    serializer = TaskSerializer(instance=task, context=context)
    todos = serializer.get_todos(task)
    count = serializer.get_todos_count(task)
    assert todos == []
    assert count == 0


def test_get_todos_and_count_without_request_in_context():
    """Ensure serializer behaves when request is absent from context."""
    user = User.objects.create_user(username="noctx", password="pw")
    task = Task.objects.create(title="TaskNoCtx", user=user)
    Todo.objects.create(title="T2", user=user, task=task)

    serializer = TaskSerializer(instance=task, context={})

    assert serializer.get_todos(task) == []
    assert serializer.get_todos_count(task) == 0
