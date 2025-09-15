"""
Test cases for Todo application.

This module contains unit tests for the Todo API endpoints and functionality.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Todo


class TodoAPITest(TestCase):
    """Test cases for Todo API endpoints."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass123'
        )

    def test_create_todo_minimal(self):
        """Test creating a todo with minimal data."""
        # Force authentication
        self.client.force_authenticate(user=self.user)
        
        url = reverse('todo-list')
        data = {'title': 'Buy milk'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Todo.objects.count(), 1)
        
        todo = Todo.objects.first()
        self.assertEqual(todo.title, 'Buy milk')

    def test_create_todo_with_user_and_tags(self):
        """Test creating a todo with user association and tags."""
        # Force authentication
        self.client.force_authenticate(user=self.user)
        
        url = reverse('todo-list')
        data = {
            'title': 'Write tests',
            'tags': ['work', 'urgent'],
            'user': [self.user.id],
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 201)
        
        todo = Todo.objects.get(title='Write tests')
        self.assertIn('work', todo.tags)
        self.assertEqual(list(todo.user.all()), [self.user])

    def test_todo_str_representation(self):
        """Test the string representation of Todo model."""
        todo = Todo.objects.create(title='Test Todo')
        self.assertEqual(str(todo), 'Test Todo')

    def test_todo_str_representation_long_title(self):
        """Test string representation with long title."""
        long_title = 'a' * 60
        todo = Todo.objects.create(title=long_title)
        expected = f"{'a' * 50}..."
        self.assertEqual(str(todo), expected)
