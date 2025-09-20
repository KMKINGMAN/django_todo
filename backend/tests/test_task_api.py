"""
API tests for Task endpoints.

This module contains comprehensive tests for the Task API endpoints
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
class TestTaskAPI:
    """Test cases for Task API endpoints."""

    def test_unauthenticated_access_denied(self, api_client):
        """Test that unauthenticated requests are denied."""
        url = reverse("task-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_tasks_empty(self, authenticated_client):
        """Test listing tasks when user has no tasks."""
        url = reverse("task-list")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_create_task(self, authenticated_client, user):
        """Test creating a new task."""
        task_data = {"title": "Test Task", "description": "Test Task Description"}

        url = reverse("task-list")
        response = authenticated_client.post(url, task_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == task_data["title"]
        assert response.data["description"] == task_data["description"]
        assert "todos_count" in response.data
        assert response.data["todos_count"] == 0
        # Note: 'todos' field is not included by default, only with include_todos=1

        # Verify task was created in database
        task = Task.objects.get(id=response.data["id"])
        assert task.user == user
        assert task.title == task_data["title"]

    def test_create_task_minimal_data(self, authenticated_client, user):
        """Test creating a task with only required fields."""
        task_data = {"title": "Minimal Task"}

        url = reverse("task-list")
        response = authenticated_client.post(url, task_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == task_data["title"]
        assert response.data["description"] is None

        # Verify task was created
        task = Task.objects.get(id=response.data["id"])
        assert task.user == user

    def test_create_task_missing_title(self, authenticated_client):
        """Test creating a task without title fails."""
        task_data = {"description": "Description without title"}

        url = reverse("task-list")
        response = authenticated_client.post(url, task_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_user_tasks_only(self, authenticated_client, user):
        """Test that users only see their own tasks."""
        # Create another user and their task
        other_user = User.objects.create_user(username="otheruser", password="pass123")
        Task.objects.create(title="Other User Task", user=other_user)

        # Create task for authenticated user
        Task.objects.create(title="My Task", user=user)

        url = reverse("task-list")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["title"] == "My Task"

    def test_retrieve_task(self, authenticated_client, user):
        """Test retrieving a specific task."""
        task = Task.objects.create(
            title="Specific Task", description="Specific Description", user=user
        )

        url = reverse("task-detail", kwargs={"pk": task.id})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == task.id
        assert response.data["title"] == task.title
        assert response.data["description"] == task.description

    def test_retrieve_task_with_todos(self, authenticated_client, user):
        """Test retrieving a task that has associated todos."""
        task = Task.objects.create(title="Task with Todos", user=user)

        # Create todos associated with this task
        _todo1 = Todo.objects.create(title="Todo 1", task=task, user=user)
        _todo2 = Todo.objects.create(title="Todo 2", task=task, user=user)

        # Test with include_todos=1 to get the todos in response
        url = reverse("task-detail", kwargs={"pk": task.id})
        response = authenticated_client.get(url, {"include_todos": "1"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["todos"]) == 2

        # Verify todos are included
        todo_titles = [todo["title"] for todo in response.data["todos"]]
        assert "Todo 1" in todo_titles
        assert "Todo 2" in todo_titles

    def test_retrieve_other_user_task_forbidden(self, authenticated_client):
        """Test that users cannot retrieve other users' tasks."""
        other_user = User.objects.create_user(username="otheruser", password="pass123")
        other_task = Task.objects.create(title="Other User Task", user=other_user)

        url = reverse("task-detail", kwargs={"pk": other_task.id})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_task(self, authenticated_client, user):
        """Test updating a task."""
        task = Task.objects.create(
            title="Original Title", description="Original Description", user=user
        )

        update_data = {"title": "Updated Title", "description": "Updated Description"}

        url = reverse("task-detail", kwargs={"pk": task.id})
        response = authenticated_client.put(url, update_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == update_data["title"]
        assert response.data["description"] == update_data["description"]

        # Verify database was updated
        task.refresh_from_db()
        assert task.title == update_data["title"]
        assert task.description == update_data["description"]

    def test_partial_update_task(self, authenticated_client, user):
        """Test partially updating a task."""
        task = Task.objects.create(
            title="Original Title", description="Original Description", user=user
        )

        update_data = {"title": "Updated Title Only"}

        url = reverse("task-detail", kwargs={"pk": task.id})
        response = authenticated_client.patch(url, update_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == update_data["title"]
        assert response.data["description"] == "Original Description"  # Unchanged

    def test_delete_task_without_todos(self, authenticated_client, user):
        """Test deleting a task that has no associated todos."""
        task = Task.objects.create(title="Task to Delete", user=user)

        url = reverse("task-detail", kwargs={"pk": task.id})
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify task was deleted
        assert not Task.objects.filter(id=task.id).exists()

    def test_delete_task_with_todos(self, authenticated_client, user):
        """Test deleting a task that has associated todos."""
        task = Task.objects.create(title="Task with Todos", user=user)

        # Create todos associated with this task
        todo1 = Todo.objects.create(title="Todo 1", task=task, user=user)
        todo2 = Todo.objects.create(title="Todo 2", task=task, user=user)

        url = reverse("task-detail", kwargs={"pk": task.id})
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify task was deleted
        assert not Task.objects.filter(id=task.id).exists()

        # Verify associated todos were also deleted
        assert not Todo.objects.filter(id=todo1.id).exists()
        assert not Todo.objects.filter(id=todo2.id).exists()

    def test_delete_other_user_task_forbidden(self, authenticated_client):
        """Test that users cannot delete other users' tasks."""
        other_user = User.objects.create_user(username="otheruser", password="pass123")
        other_task = Task.objects.create(title="Other User Task", user=other_user)

        url = reverse("task-detail", kwargs={"pk": other_task.id})
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Verify task was not deleted
        assert Task.objects.filter(id=other_task.id).exists()

    def test_superuser_can_see_all_tasks(self, authenticated_superuser_client, user):
        """Test that superuser can see all tasks from all users."""
        # Create tasks for different users
        other_user = User.objects.create_user(username="otheruser", password="pass123")

        Task.objects.create(title="User Task", user=user)
        Task.objects.create(title="Other User Task", user=other_user)

        url = reverse("task-list")
        response = authenticated_superuser_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        # Verify both tasks are present
        titles = [task["title"] for task in response.data]
        assert "User Task" in titles
        assert "Other User Task" in titles

    def test_task_ordering(self, authenticated_client, user):
        """Test that tasks are ordered by creation date (newest first)."""
        # Create tasks in sequence
        _task1 = Task.objects.create(title="First Task", user=user)
        _task2 = Task.objects.create(title="Second Task", user=user)
        _task3 = Task.objects.create(title="Third Task", user=user)

        url = reverse("task-list")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

        # Verify ordering (newest first)
        assert response.data[0]["title"] == "Third Task"
        assert response.data[1]["title"] == "Second Task"
        assert response.data[2]["title"] == "First Task"

    def test_delete_task_mixed_user_todos(self, authenticated_client, user):
        """Test deleting task behavior with todos from multiple users."""
        # Create another user
        other_user = User.objects.create_user(username="otheruser", password="pass123")

        # Create a task owned by the authenticated user
        task = Task.objects.create(title="Shared Task", user=user)

        # Create todos: one owned by authenticated user, one by other user
        user_todo = Todo.objects.create(title="User Todo", task=task, user=user)
        other_todo = Todo.objects.create(title="Other Todo", task=task, user=other_user)

        url = reverse("task-detail", kwargs={"pk": task.id})
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify task was deleted
        assert not Task.objects.filter(id=task.id).exists()

        assert not Todo.objects.filter(id=user_todo.id).exists()
        assert not Todo.objects.filter(id=other_todo.id).exists()
