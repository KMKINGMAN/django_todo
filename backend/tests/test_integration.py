"""
Integration tests for the Todo application workflow.

This module contains integration tests that verify the complete
workflow of the Todo application API including user authentication,
task creation, todo management, and cross-model interactions.
"""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from app.models import Todo, Task


@pytest.mark.django_db
@pytest.mark.integration
class TestTodoApplicationWorkflow:
    """Integration tests for complete Todo application workflows."""

    def test_complete_user_workflow(self, api_client):
        """Test a complete user workflow from registration to task completion."""
        
        # Step 1: Create a user (simulating registration)
        user = User.objects.create_user(
            username="workflowuser",
            email="workflow@example.com",
            password="workflow123"
        )
        
        # Step 2: User logs in
        login_data = {
            "username": "workflowuser",
            "password": "workflow123"
        }
        
        login_url = reverse('api_login')
        login_response = api_client.post(login_url, login_data, format='json')
        
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.data['token']
        
        # Set up authenticated client
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        
        # Step 3: User creates a task
        task_data = {
            "title": "Personal Project",
            "description": "Build a todo app with Django and React"
        }
        
        task_url = reverse('task-list')
        task_response = api_client.post(task_url, task_data, format='json')
        
        assert task_response.status_code == status.HTTP_201_CREATED
        task_id = task_response.data['id']
        assert task_response.data['title'] == task_data['title']
        
        # Step 4: User creates multiple todos for the task
        todos_data = [
            {
                "title": "Set up Django backend",
                "description": "Configure Django with DRF",
                "task": task_id,
                "tags": ["backend", "django"]
            },
            {
                "title": "Create React frontend",
                "description": "Set up React with necessary components", 
                "task": task_id,
                "tags": ["frontend", "react"]
            },
            {
                "title": "Write API tests",
                "description": "Create comprehensive test coverage",
                "task": task_id,
                "tags": ["testing", "api"]
            }
        ]
        
        todo_url = reverse('todo-list')
        created_todos = []
        
        for todo_data in todos_data:
            todo_response = api_client.post(todo_url, todo_data, format='json')
            assert todo_response.status_code == status.HTTP_201_CREATED
            assert todo_response.data['task'] == task_id
            created_todos.append(todo_response.data)
        
        # Step 5: User retrieves the task with all todos
        task_detail_url = reverse('task-detail', kwargs={'pk': task_id})
        task_detail_response = api_client.get(
            task_detail_url, 
            {'include_todos': '1'}
        )
        
        assert task_detail_response.status_code == status.HTTP_200_OK
        assert len(task_detail_response.data['todos']) == 3
        
        # Step 6: User completes some todos
        for i, todo in enumerate(created_todos[:2]):  # Complete first 2 todos
            update_data = {"completed": True}
            todo_detail_url = reverse('todo-detail', kwargs={'pk': todo['id']})
            update_response = api_client.patch(
                todo_detail_url, 
                update_data, 
                format='json'
            )
            assert update_response.status_code == status.HTTP_200_OK
            assert update_response.data['completed'] is True
        
        # Step 7: User lists all their todos (should see completed and incomplete)
        todo_list_response = api_client.get(todo_url)
        assert todo_list_response.status_code == status.HTTP_200_OK
        assert len(todo_list_response.data) == 3
        
        # Verify 2 completed, 1 incomplete
        completed_count = sum(1 for todo in todo_list_response.data if todo['completed'])
        assert completed_count == 2
        
        # Step 8: User creates a standalone todo (without task)
        standalone_todo = {
            "title": "Learn something new",
            "description": "Read about new technologies",
            "tags": ["learning", "personal"]
        }
        
        standalone_response = api_client.post(todo_url, standalone_todo, format='json')
        assert standalone_response.status_code == status.HTTP_201_CREATED
        assert standalone_response.data['task'] is None
        
        # Step 9: User lists all tasks and todos to verify final state
        final_todo_list = api_client.get(todo_url)
        final_task_list = api_client.get(task_url)
        
        assert len(final_todo_list.data) == 4  # 3 task todos + 1 standalone
        assert len(final_task_list.data) == 1  # 1 task
        
        # Verify the task has correct todos_count
        assert final_task_list.data[0]['todos_count'] == 3

    def test_multi_user_isolation(self, api_client):
        """Test that multiple users' data is properly isolated."""
        
        # Create two users
        user1 = User.objects.create_user(username="user1", password="pass123")
        user2 = User.objects.create_user(username="user2", password="pass123")
        
        # Get tokens for both users
        token1, _ = Token.objects.get_or_create(user=user1)
        token2, _ = Token.objects.get_or_create(user=user2)
        
        # User 1 creates a task and todo
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token1.key}')
        
        task1_data = {"title": "User 1 Task"}
        task1_response = api_client.post(reverse('task-list'), task1_data, format='json')
        task1_id = task1_response.data['id']
        
        todo1_data = {"title": "User 1 Todo", "task": task1_id}
        todo1_response = api_client.post(reverse('todo-list'), todo1_data, format='json')
        
        # User 2 creates a task and todo  
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token2.key}')
        
        task2_data = {"title": "User 2 Task"}
        task2_response = api_client.post(reverse('task-list'), task2_data, format='json')
        task2_id = task2_response.data['id']
        
        todo2_data = {"title": "User 2 Todo", "task": task2_id}
        todo2_response = api_client.post(reverse('todo-list'), todo2_data, format='json')
        
        # Verify User 1 can only see their own data
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token1.key}')
        
        user1_tasks = api_client.get(reverse('task-list'))
        user1_todos = api_client.get(reverse('todo-list'))
        
        assert len(user1_tasks.data) == 1
        assert user1_tasks.data[0]['title'] == "User 1 Task"
        assert len(user1_todos.data) == 1
        assert user1_todos.data[0]['title'] == "User 1 Todo"
        
        # Verify User 2 can only see their own data
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token2.key}')
        
        user2_tasks = api_client.get(reverse('task-list'))
        user2_todos = api_client.get(reverse('todo-list'))
        
        assert len(user2_tasks.data) == 1
        assert user2_tasks.data[0]['title'] == "User 2 Task"
        assert len(user2_todos.data) == 1
        assert user2_todos.data[0]['title'] == "User 2 Todo"
        
        # Verify User 1 cannot access User 2's resources
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token1.key}')
        
        user2_task_url = reverse('task-detail', kwargs={'pk': task2_id})
        user2_todo_url = reverse('todo-detail', kwargs={'pk': todo2_response.data['id']})
        
        assert api_client.get(user2_task_url).status_code == status.HTTP_404_NOT_FOUND
        assert api_client.get(user2_todo_url).status_code == status.HTTP_404_NOT_FOUND

    def test_task_deletion_cascade(self, authenticated_client, user):
        """Test that deleting a task properly handles associated todos."""
        
        # Create a task with multiple todos
        task = Task.objects.create(title="Task to Delete", user=user)
        
        todo1 = Todo.objects.create(title="Todo 1", task=task, user=user)
        todo2 = Todo.objects.create(title="Todo 2", task=task, user=user)
        todo3 = Todo.objects.create(title="Todo 3", task=task, user=user)
        
        # Verify initial state
        assert Task.objects.filter(id=task.id).exists()
        assert Todo.objects.filter(task=task).count() == 3
        
        # Delete the task
        task_url = reverse('task-detail', kwargs={'pk': task.id})
        delete_response = authenticated_client.delete(task_url)
        
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify task and all associated todos are deleted
        assert not Task.objects.filter(id=task.id).exists()
        assert not Todo.objects.filter(id__in=[todo1.id, todo2.id, todo3.id]).exists()

    def test_superuser_access_all_data(self, api_client):
        """Test that superuser can access all users' data."""
        
        # Create regular user and superuser
        regular_user = User.objects.create_user(username="regular", password="pass123")
        superuser = User.objects.create_superuser(username="admin", password="admin123")
        
        # Regular user creates some data
        regular_token, _ = Token.objects.get_or_create(user=regular_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {regular_token.key}')
        
        task_data = {"title": "Regular User Task"}
        task_response = api_client.post(reverse('task-list'), task_data, format='json')
        
        todo_data = {"title": "Regular User Todo"}
        todo_response = api_client.post(reverse('todo-list'), todo_data, format='json')
        
        # Superuser logs in
        superuser_token, _ = Token.objects.get_or_create(user=superuser)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {superuser_token.key}')
        
        # Superuser can see all tasks and todos
        all_tasks = api_client.get(reverse('task-list'))
        all_todos = api_client.get(reverse('todo-list'))
        
        assert len(all_tasks.data) >= 1  # At least the regular user's task
        assert len(all_todos.data) >= 1  # At least the regular user's todo
        
        # Verify superuser can see regular user's data
        task_titles = [task['title'] for task in all_tasks.data]
        todo_titles = [todo['title'] for todo in all_todos.data]
        
        assert "Regular User Task" in task_titles
        assert "Regular User Todo" in todo_titles
