from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Todo


class TodoAPITest(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create_user(username='testuser', password='pass')
	def test_create_todo_minimal(self):
		url = reverse('todo-list')
		data = {
			'title': 'Buy milk',
		}
		resp = self.client.post(url, data, format='json')
		self.assertEqual(resp.status_code, 201)
		self.assertEqual(Todo.objects.count(), 1)
		todo = Todo.objects.first()
		self.assertEqual(todo.title, 'Buy milk')
	def test_create_todo_with_user_and_tags(self):
		url = reverse('todo-list')
		data = {
			'title': 'Write tests',
			'tags': ['work', 'urgent'],
			'user': [self.user.id],
		}
		resp = self.client.post(url, data, format='json')
		self.assertEqual(resp.status_code, 201)
		todo = Todo.objects.get(title='Write tests')
		self.assertIn('work', todo.tags)
		self.assertEqual(list(todo.user.all()), [self.user])
