"""
API tests for Todo endpoints.

This module contains comprehensive tests for the Todo API endpoints
including CRUD operations, authentication, and user permission checks.

We disable some pylint checks in this test module:
- E1101: false positives for Django model managers (e.g. `Model.objects`)
- E0401: import-error for pytest in test environment
"""

# pylint: disable=E1101,E0401

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from app.models import Todo, Task


@pytest.mark.django_db
@pytest.mark.api
class TestTodoAPI:
    """Test cases for Todo API endpoints."""

    def test_unauthenticated_access_denied(self, api_client):
        """Test that unauthenticated requests are denied."""
        url = reverse("todo-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_todos_empty(self, authenticated_client):
        """Test listing todos when user has no todos."""
        url = reverse("todo-list")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_create_todo_without_task(self, authenticated_client, user):
        """Test creating a todo without associating it with a task."""
        todo_data = {
            "title": "Test Todo",
            "description": "Test Description",
            "tags": ["test", "api"],
        }

        url = reverse("todo-list")
        response = authenticated_client.post(url, todo_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == todo_data["title"]
        assert response.data["description"] == todo_data["description"]
        assert response.data["completed"] is False
        assert response.data["tags"] == todo_data["tags"]
        assert response.data["task"] is None

        # Verify todo was created in database
        todo = Todo.objects.get(id=response.data["id"])
        assert todo.user == user
        assert todo.title == todo_data["title"]

    def test_create_todo_with_task(self, authenticated_client, user):
        """Test creating a todo and associating it with a task."""
        # Create a task first
        task = Task.objects.create(
            title="Test Task", description="Test Task Description", user=user
        )

        todo_data = {
            "title": "Test Todo with Task",
            "description": "Test Description",
            "task": task.id,
            "tags": ["task", "associated"],
        }

        url = reverse("todo-list")
        response = authenticated_client.post(url, todo_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == todo_data["title"]
        assert response.data["task"] == task.id

        # Verify todo was created and associated with task
        todo = Todo.objects.get(id=response.data["id"])
        assert todo.task == task
        assert todo.user == user

    def test_create_todo_minimal_data(self, authenticated_client, user):
        """Test creating a todo with only required fields."""
        todo_data = {"title": "Minimal Todo"}

        url = reverse("todo-list")
        response = authenticated_client.post(url, todo_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == todo_data["title"]
        assert response.data["description"] is None
        assert response.data["completed"] is False
        assert response.data["tags"] == ["general"]  # Default tags

        # Verify todo was created
        todo = Todo.objects.get(id=response.data["id"])
        assert todo.user == user

    def test_create_todo_missing_title(self, authenticated_client):
        """Test creating a todo without title fails."""
        todo_data = {"description": "Description without title"}

        url = reverse("todo-list")
        response = authenticated_client.post(url, todo_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_user_todos_only(self, authenticated_client, user):
        """Test that users only see their own todos."""
        # Create another user and their todo
        other_user = User.objects.create_user(username="otheruser", password="pass123")
        Todo.objects.create(title="Other User Todo", user=other_user)

        # Create todo for authenticated user
        Todo.objects.create(title="My Todo", user=user)

        url = reverse("todo-list")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["title"] == "My Todo"

    def test_retrieve_todo(self, authenticated_client, user):
        """Test retrieving a specific todo."""
        todo = Todo.objects.create(
            title="Specific Todo", description="Specific Description", user=user
        )

        url = reverse("todo-detail", kwargs={"pk": todo.id})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == todo.id
        assert response.data["title"] == todo.title
        assert response.data["description"] == todo.description

    def test_retrieve_other_user_todo_forbidden(self, authenticated_client):
        """Test that users cannot retrieve other users' todos."""
        other_user = User.objects.create_user(username="otheruser", password="pass123")
        other_todo = Todo.objects.create(title="Other User Todo", user=other_user)

        url = reverse("todo-detail", kwargs={"pk": other_todo.id})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_todo(self, authenticated_client, user):
        """Test updating a todo."""
        todo = Todo.objects.create(
            title="Original Title", description="Original Description", user=user
        )

        update_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "completed": True,
            "tags": ["updated", "test"],
        }

        url = reverse("todo-detail", kwargs={"pk": todo.id})
        response = authenticated_client.put(url, update_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == update_data["title"]
        assert response.data["description"] == update_data["description"]
        assert response.data["completed"] is True
        assert response.data["tags"] == update_data["tags"]

        # Verify database was updated
        todo.refresh_from_db()
        assert todo.title == update_data["title"]
        assert todo.completed is True

    def test_partial_update_todo(self, authenticated_client, user):
        """Test partially updating a todo."""
        todo = Todo.objects.create(
            title="Original Title",
            description="Original Description",
            completed=False,
            user=user,
        )

        update_data = {"completed": True}

        url = reverse("todo-detail", kwargs={"pk": todo.id})
        response = authenticated_client.patch(url, update_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["completed"] is True
        assert response.data["title"] == "Original Title"  # Unchanged
        assert response.data["description"] == "Original Description"  # Unchanged

    def test_delete_todo(self, authenticated_client, user):
        """Test deleting a todo."""
        todo = Todo.objects.create(title="Todo to Delete", user=user)

        url = reverse("todo-detail", kwargs={"pk": todo.id})
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify todo was deleted
        assert not Todo.objects.filter(id=todo.id).exists()

    def test_delete_other_user_todo_forbidden(self, authenticated_client):
        """Test that users cannot delete other users' todos."""
        other_user = User.objects.create_user(username="otheruser", password="pass123")
        other_todo = Todo.objects.create(title="Other User Todo", user=other_user)

        url = reverse("todo-detail", kwargs={"pk": other_todo.id})
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Verify todo was not deleted
        assert Todo.objects.filter(id=other_todo.id).exists()

    def test_superuser_can_see_all_todos(self, authenticated_superuser_client, user):
        """Test that superuser can see all todos from all users."""
        # Create todos for different users
        other_user = User.objects.create_user(username="otheruser", password="pass123")

        Todo.objects.create(title="User Todo", user=user)
        Todo.objects.create(title="Other User Todo", user=other_user)

        url = reverse("todo-list")
        response = authenticated_superuser_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        # Verify both todos are present
        titles = [todo["title"] for todo in response.data]
        assert "User Todo" in titles
        assert "Other User Todo" in titles

    def test_todo_ordering(self, authenticated_client, user):
        """Test that todos are ordered by creation date (newest first)."""
        # Create todos in sequence
        _todo1 = Todo.objects.create(title="First Todo", user=user)
        _todo2 = Todo.objects.create(title="Second Todo", user=user)
        _todo3 = Todo.objects.create(title="Third Todo", user=user)

        url = reverse("todo-list")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

        # Verify ordering (newest first)
        assert response.data[0]["title"] == "Third Todo"
        assert response.data[1]["title"] == "Second Todo"
        assert response.data[2]["title"] == "First Todo"
