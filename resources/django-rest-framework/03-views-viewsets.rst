===========================
Views and ViewSets Guide
===========================

Views are the controllers of your Django REST Framework API. They handle incoming requests, process data through serializers, and return appropriate responses.

🎯 Understanding Views in DRF
=============================

DRF provides several types of views, from simple function-based views to powerful ViewSets that handle complete CRUD operations with minimal code.

**View Hierarchy:**

.. code-block:: text

    APIView (Base)
    ├── Generic Views
    │   ├── ListAPIView
    │   ├── CreateAPIView
    │   ├── RetrieveAPIView
    │   ├── UpdateAPIView
    │   ├── DestroyAPIView
    │   └── Combined Views
    └── ViewSets
        ├── ViewSet
        ├── GenericViewSet
        └── ModelViewSet

📝 Function-Based Views
=======================

Simple and straightforward, perfect for custom logic:

.. code-block:: python

    from rest_framework.decorators import api_view, permission_classes
    from rest_framework.permissions import IsAuthenticated
    from rest_framework.response import Response
    from rest_framework import status
    from .models import Task
    from .serializers import TaskSerializer

    @api_view(['GET', 'POST'])
    @permission_classes([IsAuthenticated])
    def task_list(request):
        """List all tasks or create a new task."""
        
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

    @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
    @permission_classes([IsAuthenticated])
    def task_detail(request, pk):
        """Retrieve, update or delete a task."""
        
        try:
            task = Task.objects.get(pk=pk, user=request.user)
        except Task.DoesNotExist:
            return Response(
                {'error': 'Task not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if request.method == 'GET':
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = TaskSerializer(task, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

🏗️ Class-Based Views (APIView)
==============================

More structured approach with better code organization:

.. code-block:: python

    from rest_framework.views import APIView
    from rest_framework.response import Response
    from rest_framework import status
    from rest_framework.permissions import IsAuthenticated
    from django.shortcuts import get_object_or_404

    class TaskListView(APIView):
        """List all tasks or create a new task."""
        permission_classes = [IsAuthenticated]
        
        def get(self, request):
            """Get all tasks for the authenticated user."""
            tasks = Task.objects.filter(user=request.user)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        
        def post(self, request):
            """Create a new task."""
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    class TaskDetailView(APIView):
        """Retrieve, update or delete a task instance."""
        permission_classes = [IsAuthenticated]
        
        def get_object(self, pk, user):
            """Get task object or raise 404."""
            return get_object_or_404(Task, pk=pk, user=user)
        
        def get(self, request, pk):
            """Retrieve a task."""
            task = self.get_object(pk, request.user)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        
        def put(self, request, pk):
            """Update a task."""
            task = self.get_object(pk, request.user)
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        def patch(self, request, pk):
            """Partially update a task."""
            task = self.get_object(pk, request.user)
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        def delete(self, request, pk):
            """Delete a task."""
            task = self.get_object(pk, request.user)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

🧱 Generic Views
================

DRF provides pre-built generic views for common patterns:

Single-Purpose Generic Views
----------------------------

.. code-block:: python

    from rest_framework import generics
    from rest_framework.permissions import IsAuthenticated

    class TaskListView(generics.ListCreateAPIView):
        """List all tasks or create a new task."""
        serializer_class = TaskSerializer
        permission_classes = [IsAuthenticated]
        
        def get_queryset(self):
            return Task.objects.filter(user=self.request.user)
        
        def perform_create(self, serializer):
            serializer.save(user=self.request.user)

    class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
        """Retrieve, update or delete a task."""
        serializer_class = TaskSerializer
        permission_classes = [IsAuthenticated]
        
        def get_queryset(self):
            return Task.objects.filter(user=self.request.user)

Available Generic Views
-----------------------

.. code-block:: python

    # Read-only views
    from rest_framework import generics

    generics.ListAPIView          # GET /tasks/
    generics.RetrieveAPIView      # GET /tasks/1/

    # Write-only views
    generics.CreateAPIView        # POST /tasks/
    generics.UpdateAPIView        # PUT /tasks/1/
    generics.DestroyAPIView       # DELETE /tasks/1/

    # Combined views
    generics.ListCreateAPIView             # GET, POST /tasks/
    generics.RetrieveUpdateAPIView         # GET, PUT, PATCH /tasks/1/
    generics.RetrieveDestroyAPIView        # GET, DELETE /tasks/1/
    generics.RetrieveUpdateDestroyAPIView  # GET, PUT, PATCH, DELETE /tasks/1/

🎯 ViewSets (Recommended)
=========================

ViewSets group related views together and provide automatic URL routing:

Basic ViewSet
-------------

.. code-block:: python

    from rest_framework import viewsets
    from rest_framework.decorators import action
    from rest_framework.response import Response

    class TaskViewSet(viewsets.ViewSet):
        """A simple ViewSet for listing or creating tasks."""
        permission_classes = [IsAuthenticated]
        
        def list(self, request):
            """List all tasks."""
            tasks = Task.objects.filter(user=request.user)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        
        def create(self, request):
            """Create a new task."""
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        def retrieve(self, request, pk=None):
            """Retrieve a task."""
            task = get_object_or_404(Task, pk=pk, user=request.user)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        
        def update(self, request, pk=None):
            """Update a task."""
            task = get_object_or_404(Task, pk=pk, user=request.user)
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        def destroy(self, request, pk=None):
            """Delete a task."""
            task = get_object_or_404(Task, pk=pk, user=request.user)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

ModelViewSet (Most Powerful)
----------------------------

.. code-block:: python

    from rest_framework import viewsets
    from rest_framework.decorators import action
    from rest_framework.response import Response
    from rest_framework.permissions import IsAuthenticated

    class TaskViewSet(viewsets.ModelViewSet):
        """Complete CRUD operations for Task model."""
        serializer_class = TaskSerializer
        permission_classes = [IsAuthenticated]
        
        def get_queryset(self):
            """Return tasks for the current user only."""
            return Task.objects.filter(user=self.request.user)
        
        def perform_create(self, serializer):
            """Set the user when creating a task."""
            serializer.save(user=self.request.user)
        
        @action(detail=True, methods=['get'])
        def todos(self, request, pk=None):
            """Get all todos for a specific task."""
            task = self.get_object()
            todos = task.todos.all()
            serializer = TodoSerializer(todos, many=True)
            return Response(serializer.data)
        
        @action(detail=True, methods=['post'])
        def mark_complete(self, request, pk=None):
            """Mark a task as complete."""
            task = self.get_object()
            task.completed = True
            task.save()
            return Response({'status': 'task marked as complete'})
        
        @action(detail=False, methods=['get'])
        def completed(self, request):
            """Get all completed tasks."""
            completed_tasks = self.get_queryset().filter(completed=True)
            serializer = self.get_serializer(completed_tasks, many=True)
            return Response(serializer.data)

🏗️ Our Todo App ViewSets
=========================

Task ViewSet
------------

.. code-block:: python

    from rest_framework import viewsets, status
    from rest_framework.decorators import action
    from rest_framework.response import Response
    from rest_framework.permissions import IsAuthenticated
    from app.models.task_model import Task
    from app.models.todo_model import Todo
    from app.serializers.task_serializer import TaskSerializer
    from app.serializers.todo_serializer import TodoSerializer

    class TaskViewSet(viewsets.ModelViewSet):
        """ViewSet for Task model with todo management."""
        
        serializer_class = TaskSerializer
        permission_classes = [IsAuthenticated]
        
        def get_queryset(self):
            """Return tasks for the authenticated user only."""
            return Task.objects.filter(user=self.request.user)
        
        def perform_create(self, serializer):
            """Automatically set the user when creating a task."""
            serializer.save(user=self.request.user)
        
        @action(detail=True, methods=['get'])
        def todos(self, request, pk=None):
            """
            Get all todos associated with this task.
            
            GET /api/tasks/1/todos/
            """
            task = self.get_object()
            todos = Todo.objects.filter(task=task)
            serializer = TodoSerializer(todos, many=True)
            return Response(serializer.data)
        
        @action(detail=True, methods=['post'])
        def create_todo(self, request, pk=None):
            """
            Create a new todo for this task.
            
            POST /api/tasks/1/create_todo/
            {
                "title": "Todo title",
                "description": "Todo description"
            }
            """
            task = self.get_object()
            serializer = TodoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, task=task)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        @action(detail=False, methods=['get'])
        def completed(self, request):
            """
            Get all completed tasks for the user.
            
            GET /api/tasks/completed/
            """
            completed_tasks = self.get_queryset().filter(completed=True)
            serializer = self.get_serializer(completed_tasks, many=True)
            return Response(serializer.data)

Todo ViewSet
------------

.. code-block:: python

    class TodoViewSet(viewsets.ModelViewSet):
        """ViewSet for Todo model with completion tracking."""
        
        serializer_class = TodoSerializer
        permission_classes = [IsAuthenticated]
        
        def get_queryset(self):
            """Return todos for the authenticated user only."""
            queryset = Todo.objects.filter(user=self.request.user)
            
            # Filter by task if provided
            task_id = self.request.query_params.get('task', None)
            if task_id is not None:
                queryset = queryset.filter(task_id=task_id)
            
            # Filter by completion status
            completed = self.request.query_params.get('completed', None)
            if completed is not None:
                queryset = queryset.filter(completed=completed.lower() == 'true')
            
            return queryset
        
        def perform_create(self, serializer):
            """Automatically set the user when creating a todo."""
            serializer.save(user=self.request.user)
        
        @action(detail=True, methods=['post'])
        def toggle_complete(self, request, pk=None):
            """
            Toggle the completion status of a todo.
            
            POST /api/todos/1/toggle_complete/
            """
            todo = self.get_object()
            todo.completed = not todo.completed
            todo.save()
            
            return Response({
                'id': todo.id,
                'completed': todo.completed,
                'message': f'Todo marked as {"completed" if todo.completed else "incomplete"}'
            })
        
        @action(detail=False, methods=['get'])
        def by_task(self, request):
            """
            Get todos grouped by task.
            
            GET /api/todos/by_task/
            """
            todos_by_task = {}
            todos = self.get_queryset().select_related('task')
            
            for todo in todos:
                task_title = todo.task.title if todo.task else 'No Task'
                if task_title not in todos_by_task:
                    todos_by_task[task_title] = []
                todos_by_task[task_title].append(TodoSerializer(todo).data)
            
            return Response(todos_by_task)

🔄 Custom Actions
=================

ViewSets support custom actions beyond CRUD operations:

Action Types
------------

.. code-block:: python

    from rest_framework.decorators import action

    class TaskViewSet(viewsets.ModelViewSet):
        
        @action(detail=True, methods=['post'])
        def set_priority(self, request, pk=None):
            """Set task priority (detail action - requires pk)."""
            task = self.get_object()
            priority = request.data.get('priority')
            if priority in [1, 2, 3, 4, 5]:
                task.priority = priority
                task.save()
                return Response({'status': f'priority set to {priority}'})
            return Response(
                {'error': 'Priority must be 1-5'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        @action(detail=False, methods=['get'])
        def statistics(self, request):
            """Get task statistics (list action - no pk needed)."""
            queryset = self.get_queryset()
            total_tasks = queryset.count()
            completed_tasks = queryset.filter(completed=True).count()
            
            return Response({
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            })
        
        @action(detail=False, methods=['post'])
        def bulk_create(self, request):
            """Create multiple tasks at once."""
            tasks_data = request.data.get('tasks', [])
            created_tasks = []
            
            for task_data in tasks_data:
                serializer = self.get_serializer(data=task_data)
                if serializer.is_valid():
                    task = serializer.save(user=request.user)
                    created_tasks.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(created_tasks, status=status.HTTP_201_CREATED)

URL Patterns for Actions
------------------------

Custom actions automatically generate URLs:

.. code-block:: python

    # Generated URLs for TaskViewSet actions:
    
    # Standard CRUD
    GET    /api/tasks/              # list
    POST   /api/tasks/              # create
    GET    /api/tasks/{id}/         # retrieve
    PUT    /api/tasks/{id}/         # update
    PATCH  /api/tasks/{id}/         # partial_update
    DELETE /api/tasks/{id}/         # destroy
    
    # Custom actions
    POST   /api/tasks/{id}/set_priority/     # detail action
    GET    /api/tasks/statistics/            # list action
    POST   /api/tasks/bulk_create/           # list action
    GET    /api/tasks/{id}/todos/            # detail action
    POST   /api/tasks/{id}/create_todo/      # detail action

🎨 Advanced ViewSet Features
============================

Multiple Serializers
--------------------

.. code-block:: python

    class TaskViewSet(viewsets.ModelViewSet):
        permission_classes = [IsAuthenticated]
        
        def get_serializer_class(self):
            """Return different serializers for different actions."""
            if self.action == 'list':
                return TaskListSerializer      # Minimal data for list
            elif self.action == 'retrieve':
                return TaskDetailSerializer    # Full data for detail
            elif self.action in ['create', 'update', 'partial_update']:
                return TaskWriteSerializer     # Fields for writing
            return TaskSerializer
        
        def get_queryset(self):
            """Optimize queries based on action."""
            queryset = Task.objects.filter(user=self.request.user)
            
            if self.action == 'list':
                # For list view, we don't need related data
                return queryset.only('id', 'title', 'created_at')
            elif self.action == 'retrieve':
                # For detail view, prefetch related todos
                return queryset.prefetch_related('todos')
            
            return queryset

Permission per Action
--------------------

.. code-block:: python

    from rest_framework.permissions import IsAuthenticated, AllowAny

    class TaskViewSet(viewsets.ModelViewSet):
        
        def get_permissions(self):
            """Different permissions for different actions."""
            if self.action == 'list':
                # Anyone can view the list (for public tasks)
                permission_classes = [AllowAny]
            elif self.action in ['create', 'update', 'partial_update', 'destroy']:
                # Only authenticated users can modify
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [IsAuthenticated]
            
            return [permission() for permission in permission_classes]

Filtering and Pagination
------------------------

.. code-block:: python

    from django_filters.rest_framework import DjangoFilterBackend
    from rest_framework import filters

    class TaskViewSet(viewsets.ModelViewSet):
        serializer_class = TaskSerializer
        permission_classes = [IsAuthenticated]
        filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
        
        # Field-based filtering
        filterset_fields = ['completed', 'priority']
        
        # Text search
        search_fields = ['title', 'description']
        
        # Ordering
        ordering_fields = ['created_at', 'updated_at', 'priority']
        ordering = ['-created_at']  # Default ordering
        
        def get_queryset(self):
            queryset = Task.objects.filter(user=self.request.user)
            
            # Custom filtering
            due_soon = self.request.query_params.get('due_soon', None)
            if due_soon is not None:
                from django.utils import timezone
                from datetime import timedelta
                
                tomorrow = timezone.now().date() + timedelta(days=1)
                queryset = queryset.filter(due_date__lte=tomorrow, due_date__gte=timezone.now().date())
            
            return queryset

🔗 URL Configuration
====================

Router Setup
------------

.. code-block:: python

    # urls.py
    from rest_framework.routers import DefaultRouter
    from django.urls import path, include
    from app.views import TaskViewSet, TodoViewSet

    # Create router and register viewsets
    router = DefaultRouter()
    router.register(r'tasks', TaskViewSet, basename='task')
    router.register(r'todos', TodoViewSet, basename='todo')

    urlpatterns = [
        path('api/', include(router.urls)),
    ]

Generated URL Patterns
---------------------

.. code-block:: text

    # The router automatically generates these URLs:

    /api/tasks/                          # TaskViewSet
    /api/tasks/{id}/
    /api/tasks/{id}/todos/               # Custom action
    /api/tasks/{id}/create_todo/         # Custom action
    /api/tasks/completed/                # Custom action
    /api/tasks/statistics/               # Custom action

    /api/todos/                          # TodoViewSet
    /api/todos/{id}/
    /api/todos/{id}/toggle_complete/     # Custom action
    /api/todos/by_task/                  # Custom action

Manual URL Configuration
------------------------

.. code-block:: python

    # If you prefer manual URL configuration
    from django.urls import path
    from app.views import TaskViewSet, TodoViewSet

    # Extract view methods from viewsets
    task_list = TaskViewSet.as_view({'get': 'list', 'post': 'create'})
    task_detail = TaskViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })
    task_todos = TaskViewSet.as_view({'get': 'todos'})

    urlpatterns = [
        path('api/tasks/', task_list, name='task-list'),
        path('api/tasks/<int:pk>/', task_detail, name='task-detail'),
        path('api/tasks/<int:pk>/todos/', task_todos, name='task-todos'),
    ]

🧪 Testing ViewSets
===================

.. code-block:: python

    from rest_framework.test import APITestCase
    from rest_framework import status
    from django.contrib.auth.models import User
    from rest_framework.authtoken.models import Token
    from app.models import Task, Todo

    class TaskViewSetTest(APITestCase):
        def setUp(self):
            """Set up test data."""
            self.user = User.objects.create_user(
                username='testuser',
                password='testpass123'
            )
            self.token = Token.objects.create(user=self.user)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
            
            self.task = Task.objects.create(
                title='Test Task',
                description='Test Description',
                user=self.user
            )
        
        def test_list_tasks(self):
            """Test listing tasks."""
            response = self.client.get('/api/tasks/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)
        
        def test_create_task(self):
            """Test creating a new task."""
            data = {
                'title': 'New Task',
                'description': 'New Description'
            }
            response = self.client.post('/api/tasks/', data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Task.objects.count(), 2)
        
        def test_custom_action(self):
            """Test custom action."""
            response = self.client.get(f'/api/tasks/{self.task.id}/todos/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIsInstance(response.data, list)
        
        def test_unauthorized_access(self):
            """Test that unauthorized users can't access tasks."""
            self.client.credentials()  # Remove authentication
            response = self.client.get('/api/tasks/')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

🎓 Best Practices
=================

1. **Use ModelViewSet for Standard CRUD**
   - Provides complete CRUD with minimal code
   - Automatic URL routing
   - Consistent API patterns

2. **Filter Querysets by User**
   - Always filter by authenticated user
   - Prevent data leakage between users

3. **Use Custom Actions for Business Logic**
   - Keep complex operations in custom actions
   - Name actions clearly (toggle_complete, set_priority)

4. **Optimize Database Queries**
   - Use select_related and prefetch_related
   - Different querysets for different actions

5. **Handle Permissions Properly**
   - Different permissions for different actions
   - Check object-level permissions

6. **Validate Input Data**
   - Let serializers handle validation
   - Add custom validation in serializers, not views

🔍 Common Patterns
==================

User-Scoped Resources
--------------------

.. code-block:: python

    class TaskViewSet(viewsets.ModelViewSet):
        def get_queryset(self):
            return Task.objects.filter(user=self.request.user)
        
        def perform_create(self, serializer):
            serializer.save(user=self.request.user)

Soft Delete
-----------

.. code-block:: python

    class TaskViewSet(viewsets.ModelViewSet):
        def destroy(self, request, *args, **kwargs):
            """Soft delete - mark as deleted instead of removing."""
            instance = self.get_object()
            instance.is_deleted = True
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        def get_queryset(self):
            return Task.objects.filter(user=self.request.user, is_deleted=False)

Bulk Operations
---------------

.. code-block:: python

    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """Update multiple tasks at once."""
        task_updates = request.data.get('tasks', [])
        updated_tasks = []
        
        for task_update in task_updates:
            task_id = task_update.get('id')
            try:
                task = self.get_queryset().get(id=task_id)
                serializer = self.get_serializer(task, data=task_update, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    updated_tasks.append(serializer.data)
            except Task.DoesNotExist:
                continue
        
        return Response(updated_tasks)

📖 Next Steps
=============

1. 🔐 **Authentication**: Secure your API with `Authentication <./04-authentication.rst>`_
2. 🛡️ **Permissions**: Control access with `Permissions <./05-permissions.rst>`_

🔗 Resources
============

* 📚 `DRF ViewSets Documentation <https://www.django-rest-framework.org/api-guide/viewsets/>`_
* 🎯 `Generic Views <https://www.django-rest-framework.org/api-guide/generic-views/>`_
* 🔄 `Routers <https://www.django-rest-framework.org/api-guide/routers/>`_

---

ViewSets are the powerhouse of DRF, providing complete API functionality with minimal code. Master them to build efficient, maintainable APIs! 🚀

Ready to secure your API? Let's explore `Authentication <./04-authentication.rst>`_ next!