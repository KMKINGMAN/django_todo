======================================
Django REST Framework Introduction
======================================

Django REST Framework (DRF) is a powerful toolkit for building Web APIs with Django. It provides a flexible, feature-rich framework for creating RESTful APIs that can serve multiple client types (web, mobile, etc.).

🎯 What is Django REST Framework?
=================================

DRF extends Django to provide:

* 🌐 **RESTful API development** with minimal code
* 📝 **Serialization** for converting Django models to JSON/XML
* 🔐 **Authentication & Permissions** for API security
* 📊 **Browsable API** for testing and documentation
* 🧪 **Testing tools** specifically for APIs

🏗️ REST Architecture Principles
===============================

REST (Representational State Transfer) follows these principles:

HTTP Methods
------------

* **GET**: Retrieve data (read-only)
* **POST**: Create new resources
* **PUT**: Update entire resource
* **PATCH**: Partial update of resource
* **DELETE**: Remove resource

Resource-Based URLs
-------------------

.. code-block:: text

    GET    /api/tasks/           # List all tasks
    POST   /api/tasks/           # Create new task
    GET    /api/tasks/1/         # Retrieve task with ID 1
    PUT    /api/tasks/1/         # Update task with ID 1
    PATCH  /api/tasks/1/         # Partial update task with ID 1
    DELETE /api/tasks/1/         # Delete task with ID 1

Status Codes
------------

* **200 OK**: Success
* **201 Created**: Resource created
* **400 Bad Request**: Invalid data
* **401 Unauthorized**: Authentication required
* **403 Forbidden**: Permission denied
* **404 Not Found**: Resource doesn't exist
* **500 Internal Server Error**: Server error

🚀 Getting Started with DRF
===========================

Installation
------------

.. code-block:: bash

    pip install djangorestframework

Settings Configuration
----------------------

.. code-block:: python

    # settings.py
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',  # Add DRF
        'your_app',
    ]

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.TokenAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 20,
    }

📝 Serializers - Data Conversion
================================

Serializers convert Django models to JSON and validate incoming data:

Basic Serializer
----------------

.. code-block:: python

    from rest_framework import serializers
    from .models import Task

    class TaskSerializer(serializers.ModelSerializer):
        class Meta:
            model = Task
            fields = ['id', 'title', 'description', 'created_at', 'completed']
            read_only_fields = ['id', 'created_at']

Custom Serializer Fields
------------------------

.. code-block:: python

    class TaskSerializer(serializers.ModelSerializer):
        # Custom field
        days_since_created = serializers.SerializerMethodField()
        
        # Nested relationship
        user_username = serializers.CharField(source='user.username', read_only=True)
        
        class Meta:
            model = Task
            fields = ['id', 'title', 'description', 'created_at', 'completed', 
                     'days_since_created', 'user_username']
        
        def get_days_since_created(self, obj):
            from django.utils import timezone
            return (timezone.now() - obj.created_at).days

👀 Views - API Endpoints
========================

DRF provides several types of views:

Function-Based Views
--------------------

.. code-block:: python

    from rest_framework.decorators import api_view, permission_classes
    from rest_framework.permissions import IsAuthenticated
    from rest_framework.response import Response
    from rest_framework import status

    @api_view(['GET', 'POST'])
    @permission_classes([IsAuthenticated])
    def task_list(request):
        if request.method == 'GET':
            tasks = Task.objects.filter(user=request.user)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

Class-Based Views
-----------------

.. code-block:: python

    from rest_framework.views import APIView
    from rest_framework.response import Response
    from rest_framework import status

    class TaskListView(APIView):
        permission_classes = [IsAuthenticated]
        
        def get(self, request):
            tasks = Task.objects.filter(user=request.user)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        
        def post(self, request):
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

ViewSets (Recommended)
---------------------

.. code-block:: python

    from rest_framework import viewsets
    from rest_framework.decorators import action
    from rest_framework.response import Response

    class TaskViewSet(viewsets.ModelViewSet):
        serializer_class = TaskSerializer
        permission_classes = [IsAuthenticated]
        
        def get_queryset(self):
            return Task.objects.filter(user=self.request.user)
        
        def perform_create(self, serializer):
            serializer.save(user=self.request.user)
        
        @action(detail=True, methods=['post'])
        def toggle_complete(self, request, pk=None):
            task = self.get_object()
            task.completed = not task.completed
            task.save()
            return Response({'completed': task.completed})

🔗 URL Routing
==============

Manual URL Patterns
-------------------

.. code-block:: python

    from django.urls import path
    from . import views

    urlpatterns = [
        path('tasks/', views.TaskListView.as_view(), name='task-list'),
        path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    ]

Router (For ViewSets)
--------------------

.. code-block:: python

    from rest_framework.routers import DefaultRouter
    from django.urls import path, include
    from . import views

    router = DefaultRouter()
    router.register(r'tasks', views.TaskViewSet, basename='task')
    router.register(r'todos', views.TodoViewSet, basename='todo')

    urlpatterns = [
        path('api/', include(router.urls)),
    ]

🎯 Our Todo App API Structure
=============================

Let's examine our todo application's API:

Task API
--------

.. code-block:: python

    class TaskViewSet(viewsets.ModelViewSet):
        serializer_class = TaskSerializer
        permission_classes = [IsAuthenticated]
        
        def get_queryset(self):
            return Task.objects.filter(user=self.request.user)
        
        def perform_create(self, serializer):
            serializer.save(user=self.request.user)
        
        @action(detail=True, methods=['get'])
        def todos(self, request, pk=None):
            """Get all todos for a specific task."""
            task = self.get_object()
            todos = Todo.objects.filter(task=task)
            serializer = TodoSerializer(todos, many=True)
            return Response(serializer.data)

Todo API
--------

.. code-block:: python

    class TodoViewSet(viewsets.ModelViewSet):
        serializer_class = TodoSerializer
        permission_classes = [IsAuthenticated]
        
        def get_queryset(self):
            return Todo.objects.filter(user=self.request.user)
        
        def perform_create(self, serializer):
            serializer.save(user=self.request.user)
        
        @action(detail=True, methods=['post'])
        def toggle_complete(self, request, pk=None):
            """Toggle todo completion status."""
            todo = self.get_object()
            todo.completed = not todo.completed
            todo.save()
            return Response({'completed': todo.completed})

API Endpoints Generated
----------------------

.. code-block:: text

    GET    /api/tasks/              # List user's tasks
    POST   /api/tasks/              # Create new task
    GET    /api/tasks/{id}/         # Get specific task
    PUT    /api/tasks/{id}/         # Update task
    PATCH  /api/tasks/{id}/         # Partial update task
    DELETE /api/tasks/{id}/         # Delete task
    GET    /api/tasks/{id}/todos/   # Get todos for task

    GET    /api/todos/              # List user's todos
    POST   /api/todos/              # Create new todo
    GET    /api/todos/{id}/         # Get specific todo
    PUT    /api/todos/{id}/         # Update todo
    PATCH  /api/todos/{id}/         # Partial update todo
    DELETE /api/todos/{id}/         # Delete todo
    POST   /api/todos/{id}/toggle_complete/  # Toggle completion

🔐 Authentication
=================

Token Authentication Setup
--------------------------

.. code-block:: python

    # settings.py
    INSTALLED_APPS = [
        # ...
        'rest_framework.authtoken',
    ]

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.TokenAuthentication',
        ],
    }

.. code-block:: bash

    # Create tokens for existing users
    python manage.py drf_create_token <username>

Custom Login API
----------------

.. code-block:: python

    from rest_framework.views import APIView
    from rest_framework.response import Response
    from rest_framework import status
    from django.contrib.auth import authenticate
    from rest_framework.authtoken.models import Token

    class APILoginView(APIView):
        def post(self, request):
            username = request.data.get('username')
            password = request.data.get('password')
            
            if username and password:
                user = authenticate(username=username, password=password)
                if user:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        'token': token.key,
                        'user_id': user.id,
                        'username': user.username
                    })
                else:
                    return Response(
                        {'error': 'Invalid credentials'}, 
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            else:
                return Response(
                    {'error': 'Username and password required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

Using Authentication in Requests
--------------------------------

.. code-block:: javascript

    // Frontend usage
    const token = localStorage.getItem('auth_token');

    fetch('/api/tasks/', {
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
        }
    })

🛡️ Permissions
===============

Built-in Permissions
--------------------

.. code-block:: python

    from rest_framework.permissions import (
        IsAuthenticated,
        IsAuthenticatedOrReadOnly,
        AllowAny,
        IsAdminUser
    )

    class TaskViewSet(viewsets.ModelViewSet):
        serializer_class = TaskSerializer
        permission_classes = [IsAuthenticated]  # Only authenticated users

Custom Permissions
------------------

.. code-block:: python

    from rest_framework import permissions

    class IsOwnerOrReadOnly(permissions.BasePermission):
        """Custom permission to only allow owners to edit their tasks."""
        
        def has_object_permission(self, request, view, obj):
            # Read permissions for any request
            if request.method in permissions.SAFE_METHODS:
                return True
            
            # Write permissions only to the owner
            return obj.user == request.user

    class TaskViewSet(viewsets.ModelViewSet):
        serializer_class = TaskSerializer
        permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

📊 Browsable API
================

DRF provides a web interface for testing APIs:

.. code-block:: python

    # urls.py
    from rest_framework import urls

    urlpatterns = [
        path('api-auth/', include('rest_framework.urls')),  # Login/logout for browsable API
        path('api/', include(router.urls)),
    ]

Visit ``http://localhost:8000/api/tasks/`` in your browser to see the browsable API interface.

🧪 Testing APIs
===============

.. code-block:: python

    from rest_framework.test import APITestCase
    from rest_framework import status
    from django.contrib.auth.models import User
    from rest_framework.authtoken.models import Token
    from .models import Task

    class TaskAPITest(APITestCase):
        def setUp(self):
            self.user = User.objects.create_user(
                username='testuser',
                password='testpass123'
            )
            self.token = Token.objects.create(user=self.user)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        def test_create_task(self):
            """Test creating a task via API."""
            data = {'title': 'Test Task', 'description': 'Test Description'}
            response = self.client.post('/api/tasks/', data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Task.objects.count(), 1)
            self.assertEqual(Task.objects.get().title, 'Test Task')
        
        def test_list_tasks(self):
            """Test listing user's tasks."""
            Task.objects.create(title='Task 1', user=self.user)
            Task.objects.create(title='Task 2', user=self.user)
            
            response = self.client.get('/api/tasks/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 2)

🎓 Best Practices
=================

1. Use ViewSets for CRUD Operations
-----------------------------------

.. code-block:: python

    # Good: Full CRUD with minimal code
    class TaskViewSet(viewsets.ModelViewSet):
        serializer_class = TaskSerializer
        permission_classes = [IsAuthenticated]

2. Validate Data Properly
-------------------------

.. code-block:: python

    class TaskSerializer(serializers.ModelSerializer):
        class Meta:
            model = Task
            fields = ['title', 'description']
        
        def validate_title(self, value):
            if len(value) < 3:
                raise serializers.ValidationError("Title must be at least 3 characters.")
            return value

3. Filter Querysets by User
---------------------------

.. code-block:: python

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

4. Use Proper HTTP Status Codes
-------------------------------

.. code-block:: python

    return Response(data, status=status.HTTP_201_CREATED)  # For creation
    return Response(errors, status=status.HTTP_400_BAD_REQUEST)  # For validation errors

5. Handle Errors Gracefully
---------------------------

.. code-block:: python

    from rest_framework.exceptions import NotFound

    @action(detail=True)
    def custom_action(self, request, pk=None):
        try:
            obj = self.get_object()
            # Process object
            return Response(data)
        except SomeModel.DoesNotExist:
            raise NotFound("Resource not found")

📖 Next Steps
=============

1. 📝 **Serializers**: Deep dive into `Serializers <./02-serializers.rst>`_
2. 🏗️ **ViewSets**: Master `Views and ViewSets <./03-views-viewsets.rst>`_
3. 🔐 **Authentication**: Secure your API with `Authentication <./04-authentication.rst>`_
4. 🛡️ **Permissions**: Control access with `Permissions <./05-permissions.rst>`_

🔗 Official Resources
=====================

* 📚 `DRF Documentation <https://www.django-rest-framework.org/>`_
* 🎓 `DRF Tutorial <https://www.django-rest-framework.org/tutorial/quickstart/>`_
* 📖 `API Guide <https://www.django-rest-framework.org/api-guide/>`_

---

Django REST Framework makes building APIs enjoyable and efficient. With its powerful features and Django integration, you can create robust APIs that serve any client! 🚀

Ready to dive deeper? Let's explore `Serializers <./02-serializers.rst>`_ next!