============================================
Django Views and URLs - Request/Response Logic
============================================

Views are the brain of your Django application. They receive HTTP requests, process them (often involving models), and return HTTP responses. URLs determine which view handles each request.

🎯 What are Views?
==================

A view is a Python function or class that:

1. Takes an HTTP request as input
2. Processes the request (query database, validate data, etc.)
3. Returns an HTTP response (HTML, JSON, redirect, etc.)

.. code-block:: python

    from django.http import HttpResponse

    def hello_world(request):
        return HttpResponse("Hello, World!")

🔗 URL Routing
==============

URLs map web addresses to views:

.. code-block:: python

    # urls.py
    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.index, name='index'),
        path('hello/', views.hello_world, name='hello'),
        path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    ]

📝 Function-Based Views (FBVs)
==============================

Simple and straightforward for basic functionality:

Basic View
----------

.. code-block:: python

    from django.shortcuts import render, get_object_or_404
    from django.http import HttpResponse
    from .models import Task

    def task_list(request):
        tasks = Task.objects.all()
        return render(request, 'tasks/list.html', {'tasks': tasks})

    def task_detail(request, task_id):
        task = get_object_or_404(Task, id=task_id)
        return render(request, 'tasks/detail.html', {'task': task})

Handling Different HTTP Methods
-------------------------------

.. code-block:: python

    from django.shortcuts import render, redirect
    from django.contrib import messages
    from .models import Task
    from .forms import TaskForm

    def create_task(request):
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                messages.success(request, 'Task created successfully!')
                return redirect('task_detail', task_id=task.id)
        else:
            form = TaskForm()
        
        return render(request, 'tasks/create.html', {'form': form})

🏗️ Class-Based Views (CBVs)
===========================

More structured and reusable for complex functionality:

Generic Views
-------------

.. code-block:: python

    from django.views.generic import ListView, DetailView, CreateView
    from django.contrib.auth.mixins import LoginRequiredMixin
    from .models import Task

    class TaskListView(ListView):
        model = Task
        template_name = 'tasks/list.html'
        context_object_name = 'tasks'
        paginate_by = 10
        
        def get_queryset(self):
            return Task.objects.filter(user=self.request.user)

    class TaskDetailView(DetailView):
        model = Task
        template_name = 'tasks/detail.html'
        context_object_name = 'task'

    class TaskCreateView(LoginRequiredMixin, CreateView):
        model = Task
        fields = ['title', 'description']
        template_name = 'tasks/create.html'
        
        def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)

🎯 Our Todo App Views
=====================

Let's examine the views in our todo application:

Task Views (Function-Based)
---------------------------

.. code-block:: python

    from django.shortcuts import render, get_object_or_404
    from django.contrib.auth.decorators import login_required
    from django.http import JsonResponse
    from .models import Task, Todo

    @login_required
    def dashboard(request):
        """Main dashboard showing user's tasks and todos."""
        tasks = Task.objects.filter(user=request.user)
        todos = Todo.objects.filter(user=request.user)
        
        context = {
            'tasks': tasks,
            'todos': todos,
            'task_count': tasks.count(),
            'todo_count': todos.count(),
            'completed_todos': todos.filter(completed=True).count(),
        }
        return render(request, 'dashboard.html', context)

    @login_required
    def task_detail(request, task_id):
        """Show task details with associated todos."""
        task = get_object_or_404(Task, id=task_id, user=request.user)
        todos = Todo.objects.filter(task=task)
        
        context = {
            'task': task,
            'todos': todos,
        }
        return render(request, 'tasks/detail.html', context)

API Views (Using Django REST Framework)
---------------------------------------

.. code-block:: python

    from rest_framework import viewsets, status
    from rest_framework.decorators import action
    from rest_framework.response import Response
    from rest_framework.permissions import IsAuthenticated
    from .models import Task, Todo
    from .serializers import TaskSerializer, TodoSerializer

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

🌐 URL Patterns Deep Dive
=========================

Basic URL Patterns
------------------

.. code-block:: python

    from django.urls import path, include
    from . import views

    app_name = 'tasks'  # Namespace for URL names

    urlpatterns = [
        # Static URLs
        path('', views.task_list, name='list'),
        path('create/', views.task_create, name='create'),
        
        # Dynamic URLs with parameters
        path('<int:pk>/', views.task_detail, name='detail'),
        path('<int:pk>/edit/', views.task_edit, name='edit'),
        path('<int:pk>/delete/', views.task_delete, name='delete'),
        
        # String parameters
        path('<str:username>/tasks/', views.user_tasks, name='user_tasks'),
        
        # Multiple parameters
        path('<int:year>/<int:month>/', views.tasks_by_month, name='by_month'),
    ]

Advanced URL Patterns
---------------------

.. code-block:: python

    from django.urls import path, re_path
    from . import views

    urlpatterns = [
        # Regular expressions
        re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
        
        # Optional parameters
        path('tasks/<int:pk>/', views.task_detail, name='detail'),
        path('tasks/<int:pk>/<str:action>/', views.task_action, name='action'),
        
        # Include other URL configurations
        path('api/', include('api.urls')),
    ]

Our Todo App URLs
-----------------

.. code-block:: python

    # Main project urls.py
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('app.urls')),
        path('api/', include('app.urls')),  # API endpoints
    ]

    # App urls.py
    from django.urls import path, include
    from rest_framework.routers import DefaultRouter
    from . import views

    # API URLs using DRF router
    router = DefaultRouter()
    router.register(r'tasks', views.TaskViewSet, basename='task')
    router.register(r'todos', views.TodoViewSet, basename='todo')

    urlpatterns = [
        # Web views
        path('', views.dashboard, name='dashboard'),
        path('login/', views.CustomLoginView.as_view(), name='login'),
        path('logout/', views.CustomLogoutView.as_view(), name='logout'),
        
        # API endpoints
        path('api/', include(router.urls)),
        path('api/auth/login/', views.APILoginView.as_view(), name='api_login'),
    ]

🛡️ View Decorators and Mixins
=============================

Function-Based View Decorators
------------------------------

.. code-block:: python

    from django.contrib.auth.decorators import login_required, permission_required
    from django.views.decorators.http import require_http_methods
    from django.views.decorators.cache import cache_page

    @login_required
    @require_http_methods(["GET", "POST"])
    def task_create(request):
        # View logic here
        pass

    @permission_required('tasks.add_task')
    def admin_task_create(request):
        # Only users with permission can access
        pass

    @cache_page(60 * 15)  # Cache for 15 minutes
    def task_list(request):
        # Cached view
        pass

Class-Based View Mixins
-----------------------

.. code-block:: python

    from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
    from django.views.generic import CreateView

    class TaskCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
        model = Task
        fields = ['title', 'description']
        permission_required = 'tasks.add_task'
        
        def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)

📤 HTTP Responses
=================

Django views can return various types of responses:

HTML Responses
--------------

.. code-block:: python

    from django.shortcuts import render
    from django.template.response import TemplateResponse

    def task_list(request):
        tasks = Task.objects.all()
        return render(request, 'tasks/list.html', {'tasks': tasks})

    # Alternative
    def task_list_alt(request):
        tasks = Task.objects.all()
        return TemplateResponse(request, 'tasks/list.html', {'tasks': tasks})

JSON Responses
--------------

.. code-block:: python

    from django.http import JsonResponse
    import json

    def task_api(request):
        tasks = Task.objects.all()
        data = [{'id': t.id, 'title': t.title} for t in tasks]
        return JsonResponse({'tasks': data})

    def task_detail_api(request, task_id):
        task = get_object_or_404(Task, id=task_id)
        return JsonResponse({
            'id': task.id,
            'title': task.title,
            'completed': task.completed,
        })

Redirects
---------

.. code-block:: python

    from django.shortcuts import redirect
    from django.urls import reverse

    def task_create(request):
        if request.method == 'POST':
            # Process form
            return redirect('task_detail', task_id=task.id)
        
        # Show form
        return render(request, 'tasks/create.html')

    # Named URL redirect
    def after_login(request):
        return redirect(reverse('dashboard'))

File Downloads
--------------

.. code-block:: python

    from django.http import HttpResponse, FileResponse
    import csv

    def export_tasks_csv(request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tasks.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Title', 'Description', 'Created'])
        
        for task in Task.objects.all():
            writer.writerow([task.title, task.description, task.created_at])
        
        return response

🔍 Request Object
=================

The request object contains information about the HTTP request:

.. code-block:: python

    def my_view(request):
        # HTTP method
        if request.method == 'POST':
            # Handle POST data
            title = request.POST.get('title')
            
        elif request.method == 'GET':
            # Handle GET parameters
            search = request.GET.get('search', '')
        
        # User information
        if request.user.is_authenticated:
            user_tasks = Task.objects.filter(user=request.user)
        
        # Headers
        user_agent = request.META.get('HTTP_USER_AGENT')
        
        # Files (for file uploads)
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
        
        # Session data
        request.session['last_visit'] = timezone.now()
        
        return render(request, 'template.html')

🧪 Testing Views
================

.. code-block:: python

    from django.test import TestCase, Client
    from django.contrib.auth.models import User
    from django.urls import reverse
    from .models import Task

    class TaskViewTest(TestCase):
        def setUp(self):
            self.user = User.objects.create_user(
                username='testuser',
                password='testpass123'
            )
            self.client = Client()
        
        def test_task_list_requires_login(self):
            """Test that task list requires authentication."""
            response = self.client.get(reverse('task_list'))
            self.assertEqual(response.status_code, 302)  # Redirect to login
        
        def test_task_list_authenticated(self):
            """Test task list for authenticated user."""
            self.client.login(username='testuser', password='testpass123')
            response = self.client.get(reverse('task_list'))
            self.assertEqual(response.status_code, 200)
        
        def test_task_create_post(self):
            """Test creating a task via POST."""
            self.client.login(username='testuser', password='testpass123')
            data = {'title': 'Test Task', 'description': 'Test Description'}
            response = self.client.post(reverse('task_create'), data)
            self.assertEqual(response.status_code, 302)  # Redirect after creation
            self.assertTrue(Task.objects.filter(title='Test Task').exists())

🎓 Best Practices
=================

1. Use Appropriate View Types
-----------------------------

* **Function-based views**: Simple logic, one-off functionality
* **Class-based views**: Complex logic, reusable patterns

2. Handle Errors Gracefully
---------------------------

.. code-block:: python

    from django.shortcuts import get_object_or_404
    from django.http import Http404

    def task_detail(request, task_id):
        # Good: Returns 404 if not found
        task = get_object_or_404(Task, id=task_id, user=request.user)
        return render(request, 'tasks/detail.html', {'task': task})

3. Use URL Names, Not Hardcoded URLs
------------------------------------

.. code-block:: python

    # Good
    return redirect('task_detail', task_id=task.id)

    # Bad
    return redirect(f'/tasks/{task.id}/')

4. Validate User Permissions
----------------------------

.. code-block:: python

    @login_required
    def task_edit(request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        # Only the task owner can edit

5. Use Form Classes for Validation
----------------------------------

.. code-block:: python

    from django import forms

    class TaskForm(forms.ModelForm):
        class Meta:
            model = Task
            fields = ['title', 'description']

    def create_task(request):
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                return redirect('task_detail', task_id=task.id)

📖 Next Steps
=============

1. 🎨 **Templates**: Learn to display data with `Django Templates <./04-templates.rst>`_
2. 🔧 **Admin**: Manage your models with `Django Admin <./05-admin.rst>`_
3. 🌐 **REST APIs**: Build APIs with `Django REST Framework <../django-rest-framework/01-introduction.rst>`_

🔗 Further Reading
==================

* 📚 `View Documentation <https://docs.djangoproject.com/en/stable/topics/http/views/>`_
* 🔗 `URL Dispatcher <https://docs.djangoproject.com/en/stable/topics/http/urls/>`_
* 🏗️ `Class-Based Views <https://docs.djangoproject.com/en/stable/topics/class-based-views/>`_

---

Views and URLs are the traffic controllers of your Django application. Master them to build powerful, user-friendly web applications! 🚀

Ready to learn about displaying data? Let's explore `Django Templates <./04-templates.rst>`_!