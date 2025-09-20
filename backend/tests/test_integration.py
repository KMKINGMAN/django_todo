"""Integration tests for the Todo application workflow.

This module contains integration tests that verify the complete
workflow of the Todo application API including user authentication,
task creation, todo management, and cross-model interactions.

We disable some pylint checks in this test module:
- E1101: false positives for Django model managers (e.g. `Model.objects`)
- R0914: reduce local variable count by extracting helpers
- E0401: import-error for pytest in test environment
"""

# pylint: disable=E1101,R0914,E0401

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from app.models import Todo, Task


def _login_and_authenticate(api_client, username, password):
    """Create a user with credentials, log in, and set token on client."""
    user = User.objects.create_user(username=username, password=password)
    login_url = reverse("api_login")
    resp = api_client.post(
        login_url, {"username": username, "password": password}, format="json"
    )
    assert resp.status_code == status.HTTP_200_OK
    token = resp.data["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    return user


def _create_task(api_client, title, description=None):
    data = {"title": title}
    if description is not None:
        data["description"] = description
    resp = api_client.post(reverse("task-list"), data, format="json")
    assert resp.status_code == status.HTTP_201_CREATED
    return resp.data


def _create_todo(api_client, title, task=None, description=None, tags=None):
    data = {"title": title}
    if task is not None:
        data["task"] = task
    if description is not None:
        data["description"] = description
    if tags is not None:
        data["tags"] = tags
    resp = api_client.post(reverse("todo-list"), data, format="json")
    assert resp.status_code == status.HTTP_201_CREATED
    return resp.data


@pytest.mark.django_db
@pytest.mark.integration
class TestTodoApplicationWorkflow:
    """Integration tests for complete Todo application workflows."""

    def test_complete_user_workflow(self, api_client):
        """Test a complete user workflow from registration to task completion."""

        # Login and auth
        _user = _login_and_authenticate(api_client, "workflowuser", "workflow123")

        # Create a task
        task = _create_task(api_client, "Personal Project", "Build a todo app with Django and React")
        task_id = task["id"]

        # Create multiple todos for the task
        todos_specs = [
            (
                "Set up Django backend",
                "Configure Django with DRF",
                ["backend", "django"],
            ),
            (
                "Create React frontend",
                "Set up React with necessary components",
                ["frontend", "react"],
            ),
            (
                "Write API tests",
                "Create comprehensive test coverage",
                ["testing", "api"],
            ),
        ]

        created = [
            _create_todo(
                api_client, title, task=task_id, description=desc, tags=tags
            )
            for title, desc, tags in todos_specs
        ]

        # Retrieve the task with todos included
        task_detail = api_client.get(
            reverse("task-detail", kwargs={"pk": task_id}), {"include_todos": "1"}
        )
        assert task_detail.status_code == status.HTTP_200_OK
        assert len(task_detail.data["todos"]) == 3

        # Complete first two todos
        for todo in created[:2]:
            upd = api_client.patch(
                reverse("todo-detail", kwargs={"pk": todo["id"]}),
                {"completed": True},
                format="json",
            )
            assert upd.status_code == status.HTTP_200_OK
            assert upd.data["completed"] is True

        # List todos and verify counts
        all_todos = api_client.get(reverse("todo-list"))
        assert all_todos.status_code == status.HTTP_200_OK
        assert len(all_todos.data) == 3
        assert sum(1 for t in all_todos.data if t["completed"]) == 2

        # Create standalone todo
        stand = _create_todo(
            api_client,
            "Learn something new",
            description="Read about new technologies",
            tags=["learning", "personal"],
        )
        assert stand["task"] is None

        # Final checks
        final_todos = api_client.get(reverse("todo-list"))
        final_tasks = api_client.get(reverse("task-list"))
        assert len(final_todos.data) == 4
        assert len(final_tasks.data) == 1
        assert final_tasks.data[0]["todos_count"] == 3

    def test_multi_user_isolation(self, api_client):
        """Test that multiple users' data is properly isolated."""

        # Create two users and get tokens
        user1 = User.objects.create_user(username="user1", password="pass123")
        user2 = User.objects.create_user(username="user2", password="pass123")
        token1, _ = Token.objects.get_or_create(user=user1)
        token2, _ = Token.objects.get_or_create(user=user2)

        # User 1 creates a task and todo
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token1.key}")
        t1 = _create_task(api_client, "User 1 Task")
        _create_todo(api_client, "User 1 Todo", task=t1["id"])

        # User 2 creates a task and todo
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token2.key}")
        t2 = _create_task(api_client, "User 2 Task")
        _create_todo(api_client, "User 2 Todo", task=t2["id"])

        # Verify isolation
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token1.key}")
        u1_tasks = api_client.get(reverse("task-list"))
        u1_todos = api_client.get(reverse("todo-list"))
        assert len(u1_tasks.data) == 1
        assert u1_tasks.data[0]["title"] == "User 1 Task"
        assert len(u1_todos.data) == 1

        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token2.key}")
        u2_tasks = api_client.get(reverse("task-list"))
        u2_todos = api_client.get(reverse("todo-list"))
        assert len(u2_tasks.data) == 1
        assert u2_tasks.data[0]["title"] == "User 2 Task"
        assert len(u2_todos.data) == 1

        # Ensure user1 cannot access user2's resources
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token1.key}")
        assert (
            api_client.get(reverse("task-detail", kwargs={"pk": t2["id"]})).status_code
            == status.HTTP_404_NOT_FOUND
        )
        assert (
            api_client.get(
                reverse("todo-detail", kwargs={"pk": u2_todos.data[0]["id"]})
            ).status_code
            == status.HTTP_404_NOT_FOUND
        )

    def test_task_deletion_cascade(self, authenticated_client, user):
        """Test that deleting a task properly handles associated todos."""

        task = Task.objects.create(title="Task to Delete", user=user)
        a = Todo.objects.create(title="Todo 1", task=task, user=user)
        b = Todo.objects.create(title="Todo 2", task=task, user=user)
        c = Todo.objects.create(title="Todo 3", task=task, user=user)

        assert Task.objects.filter(id=task.id).exists()
        assert Todo.objects.filter(task=task).count() == 3

        delete = authenticated_client.delete(reverse("task-detail", kwargs={"pk": task.id}))
        assert delete.status_code == status.HTTP_204_NO_CONTENT
        assert not Task.objects.filter(id=task.id).exists()
        assert not Todo.objects.filter(id__in=[a.id, b.id, c.id]).exists()

    def test_superuser_access_all_data(self, api_client):
        """Test that superuser can access all users' data."""

        regular = User.objects.create_user(username="regular", password="pass123")
        admin = User.objects.create_superuser(username="admin", password="admin123")

        # Regular user creates data
        r_token, _ = Token.objects.get_or_create(user=regular)
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {r_token.key}")
        _create_task(api_client, "Regular User Task")
        _create_todo(api_client, "Regular User Todo")

        # Superuser inspects data
        s_token, _ = Token.objects.get_or_create(user=admin)
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {s_token.key}")
        all_tasks = api_client.get(reverse("task-list"))
        all_todos = api_client.get(reverse("todo-list"))
        assert any(t["title"] == "Regular User Task" for t in all_tasks.data)
        assert any(t["title"] == "Regular User Todo" for t in all_todos.data)
