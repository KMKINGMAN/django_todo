=======================
Django Admin Guide
=======================

Django Admin is one of Django's most powerful features - a built-in administrative interface that allows you to manage your application's data without writing any additional code.

🎯 What is Django Admin?
========================

Django Admin is an automatic administrative interface for Django models. It reads metadata from your models and provides a web-based interface for:

* **CRUD Operations**: Create, Read, Update, Delete records
* **User Management**: Manage users and permissions
* **Content Management**: Edit site content
* **Data Inspection**: Browse and search data

**Key Benefits:**

* 🚀 **Zero Configuration**: Works out of the box
* 🔐 **Secure**: Built-in authentication and permissions
* 🎨 **Customizable**: Extensive customization options
* 📱 **Responsive**: Mobile-friendly interface
* 🔍 **Rich Features**: Filtering, searching, pagination

🏗️ Basic Setup
===============

Enable Admin
------------

Django Admin is enabled by default in new projects:

.. code-block:: python

    # settings.py
    INSTALLED_APPS = [
        'django.contrib.admin',        # Admin interface
        'django.contrib.auth',         # Authentication
        'django.contrib.contenttypes', # Content types
        'django.contrib.sessions',     # Sessions
        'django.contrib.messages',     # Messages framework
        # ... your apps
    ]

    # Include admin URLs
    # urls.py (project level)
    from django.contrib import admin
    from django.urls import path

    urlpatterns = [
        path('admin/', admin.site.urls),
        # ... other URLs
    ]

Create Superuser
---------------

.. code-block:: bash

    # Create admin user
    python manage.py createsuperuser

    # Follow the prompts:
    # Username: admin
    # Email: admin@example.com
    # Password: (enter secure password)

🗃️ Registering Models
=====================

Basic Registration
------------------

Register your models to make them available in admin:

.. code-block:: python

    # app/admin.py
    from django.contrib import admin
    from .models import Task, Todo

    # Simple registration
    admin.site.register(Task)
    admin.site.register(Todo)

This creates basic admin interfaces with default settings.

🎨 Customizing Admin Classes
============================

ModelAdmin Classes
------------------

Create custom admin classes for advanced functionality:

.. code-block:: python

    # app/admin.py
    from django.contrib import admin
    from .models import Task, Todo

    @admin.register(Task)
    class TaskAdmin(admin.ModelAdmin):
        """Custom admin for Task model."""
        
        # Fields to display in list view
        list_display = ['title', 'user', 'completed', 'created_at', 'todo_count']
        
        # Fields that are clickable links
        list_display_links = ['title']
        
        # Add filters in right sidebar
        list_filter = ['completed', 'created_at', 'user']
        
        # Add search functionality
        search_fields = ['title', 'description']
        
        # Pagination
        list_per_page = 25
        
        # Default ordering
        ordering = ['-created_at']
        
        # Fields for add/edit forms
        fields = ['title', 'description', 'completed', 'user']
        
        # Read-only fields
        readonly_fields = ['created_at', 'updated_at']
        
        # Custom method for todo count
        def todo_count(self, obj):
            """Display number of todos for this task."""
            return obj.todos.count()
        todo_count.short_description = 'Todos'
        
        # Filter queryset based on user
        def get_queryset(self, request):
            qs = super().get_queryset(request)
            if request.user.is_superuser:
                return qs
            return qs.filter(user=request.user)

    @admin.register(Todo)
    class TodoAdmin(admin.ModelAdmin):
        """Custom admin for Todo model."""
        
        list_display = ['title', 'task', 'user', 'completed', 'due_date', 'created_at']
        list_display_links = ['title']
        list_filter = ['completed', 'due_date', 'created_at', 'task']
        search_fields = ['title', 'description', 'task__title']
        list_per_page = 50
        ordering = ['-created_at']
        
        # Group fields in add/edit forms
        fieldsets = (
            ('Basic Information', {
                'fields': ('title', 'description', 'task', 'user')
            }),
            ('Status & Dates', {
                'fields': ('completed', 'due_date'),
                'classes': ('collapse',)  # Collapsible section
            }),
            ('Metadata', {
                'fields': ('created_at', 'updated_at'),
                'classes': ('collapse',),
                'description': 'Timestamps are automatically managed.'
            }),
        )
        
        readonly_fields = ['created_at', 'updated_at']
        
        # Bulk actions
        actions = ['mark_completed', 'mark_incomplete']
        
        def mark_completed(self, request, queryset):
            """Mark selected todos as completed."""
            updated = queryset.update(completed=True)
            self.message_user(
                request, 
                f'{updated} todos marked as completed.'
            )
        mark_completed.short_description = "Mark selected todos as completed"
        
        def mark_incomplete(self, request, queryset):
            """Mark selected todos as incomplete."""
            updated = queryset.update(completed=False)
            self.message_user(
                request, 
                f'{updated} todos marked as incomplete.'
            )
        mark_incomplete.short_description = "Mark selected todos as incomplete"

🔍 Advanced Admin Features
==========================

Inline Editing
--------------

Edit related objects on the same page:

.. code-block:: python

    class TodoInline(admin.TabularInline):
        """Inline editing for todos within task admin."""
        model = Todo
        extra = 1  # Number of empty forms to display
        fields = ['title', 'description', 'completed', 'due_date']
        readonly_fields = ['created_at']

    @admin.register(Task)
    class TaskAdmin(admin.ModelAdmin):
        list_display = ['title', 'user', 'completed', 'created_at', 'todo_count']
        list_filter = ['completed', 'created_at']
        search_fields = ['title', 'description']
        
        # Add inline editing
        inlines = [TodoInline]
        
        fieldsets = (
            ('Task Information', {
                'fields': ('title', 'description', 'user', 'completed')
            }),
            ('Timestamps', {
                'fields': ('created_at', 'updated_at'),
                'classes': ('collapse',),
            }),
        )
        
        readonly_fields = ['created_at', 'updated_at']
        
        def todo_count(self, obj):
            return obj.todos.count()
        todo_count.short_description = 'Number of Todos'

Custom List Display
------------------

.. code-block:: python

    @admin.register(Task)
    class TaskAdmin(admin.ModelAdmin):
        list_display = [
            'title', 
            'user', 
            'completion_status', 
            'progress_bar', 
            'days_since_created',
            'todo_count'
        ]
        
        def completion_status(self, obj):
            """Display completion status with colored badge."""
            if obj.completed:
                return format_html(
                    '<span style="color: green; font-weight: bold;">✅ Completed</span>'
                )
            else:
                return format_html(
                    '<span style="color: orange; font-weight: bold;">⏳ Pending</span>'
                )
        completion_status.short_description = 'Status'
        
        def progress_bar(self, obj):
            """Display progress bar for todo completion."""
            total_todos = obj.todos.count()
            if total_todos == 0:
                return format_html('<em>No todos</em>')
            
            completed_todos = obj.todos.filter(completed=True).count()
            percentage = round((completed_todos / total_todos) * 100)
            
            return format_html(
                '<div style="width: 100px; background-color: #f0f0f0; border-radius: 4px;">'
                '<div style="width: {}%; background-color: #28a745; color: white; '
                'text-align: center; border-radius: 4px; padding: 2px;">{}%</div></div>',
                percentage, percentage
            )
        progress_bar.short_description = 'Progress'
        
        def days_since_created(self, obj):
            """Display days since task was created."""
            from django.utils import timezone
            days = (timezone.now() - obj.created_at).days
            return f"{days} days ago"
        days_since_created.short_description = 'Age'
        
        def todo_count(self, obj):
            """Display todo count with link."""
            count = obj.todos.count()
            if count > 0:
                url = f"/admin/app/todo/?task__id__exact={obj.id}"
                return format_html(
                    '<a href="{}">{} todos</a>',
                    url, count
                )
            return "No todos"
        todo_count.short_description = 'Todos'

🎨 Admin Customization
======================

Custom Admin Site
-----------------

.. code-block:: python

    # admin.py
    from django.contrib import admin
    from django.contrib.admin import AdminSite

    class TodoAdminSite(AdminSite):
        """Custom admin site for Todo app."""
        site_header = '📝 Todo Application Admin'
        site_title = 'Todo Admin'
        index_title = 'Welcome to Todo Administration'
        
        def get_app_list(self, request, app_label=None):
            """
            Return a sorted list of all the installed apps.
            """
            app_list = super().get_app_list(request, app_label)
            
            # Custom ordering
            app_order = ['app', 'auth']  # Your app first, then auth
            
            return sorted(app_list, key=lambda x: app_order.index(x['app_label']) 
                         if x['app_label'] in app_order else len(app_order))

    # Create custom admin site instance
    todo_admin_site = TodoAdminSite(name='todo_admin')

    # Register models with custom site
    todo_admin_site.register(Task, TaskAdmin)
    todo_admin_site.register(Todo, TodoAdmin)

    # Also register with default admin
    admin.site.register(Task, TaskAdmin)
    admin.site.register(Todo, TodoAdmin)

Filters and Search
-----------------

.. code-block:: python

    from django.contrib import admin
    from django.utils.translation import gettext_lazy as _

    class CompletionListFilter(admin.SimpleListFilter):
        """Custom filter for task completion status."""
        title = _('completion status')
        parameter_name = 'completion'

        def lookups(self, request, model_admin):
            return (
                ('completed', _('Completed')),
                ('incomplete', _('Incomplete')),
                ('no_todos', _('No todos')),
            )

        def queryset(self, request, queryset):
            if self.value() == 'completed':
                return queryset.filter(completed=True)
            if self.value() == 'incomplete':
                return queryset.filter(completed=False)
            if self.value() == 'no_todos':
                return queryset.filter(todos__isnull=True)

    class DateRangeFilter(admin.SimpleListFilter):
        """Custom filter for date ranges."""
        title = _('creation date')
        parameter_name = 'created'

        def lookups(self, request, model_admin):
            return (
                ('today', _('Today')),
                ('week', _('This week')),
                ('month', _('This month')),
            )

        def queryset(self, request, queryset):
            from django.utils import timezone
            from datetime import timedelta
            
            now = timezone.now()
            
            if self.value() == 'today':
                return queryset.filter(created_at__date=now.date())
            if self.value() == 'week':
                week_ago = now - timedelta(days=7)
                return queryset.filter(created_at__gte=week_ago)
            if self.value() == 'month':
                month_ago = now - timedelta(days=30)
                return queryset.filter(created_at__gte=month_ago)

    @admin.register(Task)
    class TaskAdmin(admin.ModelAdmin):
        list_display = ['title', 'user', 'completed', 'created_at']
        list_filter = [CompletionListFilter, DateRangeFilter, 'user']
        search_fields = ['title', 'description', 'user__username']

🔐 Permissions and Security
===========================

Custom Permissions
------------------

.. code-box:: python

    @admin.register(Task)
    class TaskAdmin(admin.ModelAdmin):
        def get_queryset(self, request):
            """Filter queryset based on user permissions."""
            qs = super().get_queryset(request)
            
            if request.user.is_superuser:
                return qs
            
            # Regular users only see their own tasks
            return qs.filter(user=request.user)
        
        def has_change_permission(self, request, obj=None):
            """Check if user can change the object."""
            if obj is None:  # Permission for listing
                return True
            
            # Superusers can edit anything
            if request.user.is_superuser:
                return True
            
            # Users can only edit their own tasks
            return obj.user == request.user
        
        def has_delete_permission(self, request, obj=None):
            """Check if user can delete the object."""
            if obj is None:
                return request.user.is_superuser
            
            return request.user.is_superuser or obj.user == request.user
        
        def save_model(self, request, obj, form, change):
            """Set the user when saving."""
            if not change:  # Creating new object
                obj.user = request.user
            super().save_model(request, obj, form, change)

Group-Based Permissions
----------------------

.. code-block:: python

    # Create groups and permissions in Django shell or data migration
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from app.models import Task, Todo

    # Create groups
    managers_group, created = Group.objects.get_or_create(name='Task Managers')
    users_group, created = Group.objects.get_or_create(name='Regular Users')

    # Get content types
    task_ct = ContentType.objects.get_for_model(Task)
    todo_ct = ContentType.objects.get_for_model(Todo)

    # Create custom permissions
    view_all_tasks_perm = Permission.objects.create(
        codename='view_all_tasks',
        name='Can view all tasks',
        content_type=task_ct,
    )

    # Assign permissions to groups
    managers_group.permissions.add(view_all_tasks_perm)

    # In admin.py
    @admin.register(Task)
    class TaskAdmin(admin.ModelAdmin):
        def get_queryset(self, request):
            qs = super().get_queryset(request)
            
            if request.user.has_perm('app.view_all_tasks'):
                return qs  # Managers see all tasks
            
            return qs.filter(user=request.user)  # Users see only their tasks

📊 Custom Admin Views
=====================

Adding Custom Views
-------------------

.. code-block:: python

    from django.shortcuts import render
    from django.contrib.admin.views.decorators import staff_member_required
    from django.urls import path
    from django.http import JsonResponse
    from django.db.models import Count, Q

    class TaskAdmin(admin.ModelAdmin):
        # ... existing configuration
        
        def get_urls(self):
            """Add custom URLs to admin."""
            urls = super().get_urls()
            custom_urls = [
                path('statistics/', self.admin_site.admin_view(self.statistics_view), 
                     name='task_statistics'),
                path('export/', self.admin_site.admin_view(self.export_view), 
                     name='task_export'),
            ]
            return custom_urls + urls
        
        def statistics_view(self, request):
            """Display task statistics."""
            stats = {
                'total_tasks': Task.objects.count(),
                'completed_tasks': Task.objects.filter(completed=True).count(),
                'total_todos': Todo.objects.count(),
                'completed_todos': Todo.objects.filter(completed=True).count(),
            }
            
            # Tasks by user
            user_stats = Task.objects.values('user__username').annotate(
                total=Count('id'),
                completed=Count('id', filter=Q(completed=True))
            )
            
            context = {
                'title': 'Task Statistics',
                'stats': stats,
                'user_stats': user_stats,
                'opts': self.model._meta,
            }
            
            return render(request, 'admin/task_statistics.html', context)
        
        def export_view(self, request):
            """Export tasks as JSON."""
            tasks = Task.objects.select_related('user').prefetch_related('todos')
            
            data = []
            for task in tasks:
                data.append({
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'user': task.user.username,
                    'created_at': task.created_at.isoformat(),
                    'todos': [
                        {
                            'title': todo.title,
                            'completed': todo.completed,
                        }
                        for todo in task.todos.all()
                    ]
                })
            
            return JsonResponse({'tasks': data}, indent=2)

📱 Admin Templates
==================

Custom Admin Templates
----------------------

.. code-block:: html

    <!-- templates/admin/task_statistics.html -->
    {% extends "admin/base_site.html" %}
    {% load i18n static %}

    {% block title %}Task Statistics{% endblock %}

    {% block breadcrumbs %}
    <div class="breadcrumbs">
        <a href="{% url 'admin:index' %}">Home</a>
        &rsaquo; <a href="{% url 'admin:app_task_changelist' %}">Tasks</a>
        &rsaquo; Statistics
    </div>
    {% endblock %}

    {% block content %}
    <h1>📊 Task Statistics</h1>

    <div class="module">
        <h2>Overview</h2>
        <table>
            <tr>
                <th>Total Tasks:</th>
                <td>{{ stats.total_tasks }}</td>
            </tr>
            <tr>
                <th>Completed Tasks:</th>
                <td>{{ stats.completed_tasks }}</td>
            </tr>
            <tr>
                <th>Total Todos:</th>
                <td>{{ stats.total_todos }}</td>
            </tr>
            <tr>
                <th>Completed Todos:</th>
                <td>{{ stats.completed_todos }}</td>
            </tr>
        </table>
    </div>

    <div class="module">
        <h2>Tasks by User</h2>
        <table>
            <thead>
                <tr>
                    <th>User</th>
                    <th>Total Tasks</th>
                    <th>Completed</th>
                    <th>Completion Rate</th>
                </tr>
            </thead>
            <tbody>
                {% for user_stat in user_stats %}
                <tr>
                    <td>{{ user_stat.user__username }}</td>
                    <td>{{ user_stat.total }}</td>
                    <td>{{ user_stat.completed }}</td>
                    <td>
                        {% if user_stat.total > 0 %}
                            {% widthratio user_stat.completed user_stat.total 100 %}%
                        {% else %}
                            0%
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="submit-row">
        <a href="{% url 'admin:task_export' %}" class="default">Export Data</a>
    </div>
    {% endblock %}

🧪 Testing Admin
================

.. code-block:: python

    from django.test import TestCase, Client
    from django.contrib.auth.models import User
    from django.urls import reverse
    from .models import Task

    class AdminTest(TestCase):
        def setUp(self):
            """Set up test data."""
            self.admin_user = User.objects.create_superuser(
                'admin', 'admin@test.com', 'pass'
            )
            self.regular_user = User.objects.create_user(
                'user', 'user@test.com', 'pass'
            )
            self.task = Task.objects.create(
                title='Test Task',
                description='Test Description',
                user=self.regular_user
            )
            self.client = Client()
        
        def test_admin_access(self):
            """Test admin can access admin site."""
            self.client.login(username='admin', password='pass')
            response = self.client.get('/admin/')
            self.assertEqual(response.status_code, 200)
        
        def test_task_list_admin(self):
            """Test task list in admin."""
            self.client.login(username='admin', password='pass')
            url = reverse('admin:app_task_changelist')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Test Task')
        
        def test_task_edit_admin(self):
            """Test editing task in admin."""
            self.client.login(username='admin', password='pass')
            url = reverse('admin:app_task_change', args=[self.task.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            
            # Test updating task
            data = {
                'title': 'Updated Task',
                'description': 'Updated Description',
                'user': self.regular_user.id,
                'completed': True,
            }
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 302)  # Redirect after save
            
            # Verify changes
            self.task.refresh_from_db()
            self.assertEqual(self.task.title, 'Updated Task')
            self.assertTrue(self.task.completed)

🎓 Best Practices
=================

1. **Keep It Simple**
   - Don't over-customize if default behavior works
   - Focus on user experience

2. **Security First**
   - Always filter querysets by user permissions
   - Implement proper permission checks

3. **Performance Optimization**
   - Use ``select_related`` and ``prefetch_related``
   - Limit query complexity in list views

4. **User-Friendly Interface**
   - Add helpful descriptions and field labels
   - Group related fields with fieldsets

5. **Testing**
   - Test admin functionality thoroughly
   - Verify permission restrictions work

📖 Common Admin Patterns
========================

Read-Only Models
----------------

.. code-block:: python

    @admin.register(AuditLog)
    class AuditLogAdmin(admin.ModelAdmin):
        """Read-only admin for audit logs."""
        list_display = ['action', 'user', 'timestamp', 'object_repr']
        list_filter = ['action', 'timestamp']
        search_fields = ['object_repr', 'user__username']
        
        def has_add_permission(self, request):
            return False
        
        def has_change_permission(self, request, obj=None):
            return False
        
        def has_delete_permission(self, request, obj=None):
            return False

Bulk Operations
--------------

.. code-block:: python

    @admin.register(Task)
    class TaskAdmin(admin.ModelAdmin):
        actions = ['bulk_complete', 'bulk_reset', 'export_selected']
        
        def bulk_complete(self, request, queryset):
            """Mark selected tasks as completed."""
            count = queryset.update(completed=True)
            self.message_user(request, f'{count} tasks marked as completed.')
        bulk_complete.short_description = "Mark selected tasks as completed"
        
        def bulk_reset(self, request, queryset):
            """Reset selected tasks to incomplete."""
            count = queryset.update(completed=False)
            self.message_user(request, f'{count} tasks reset to incomplete.')
        bulk_reset.short_description = "Mark selected tasks as incomplete"

🔗 Resources
============

* 📚 `Django Admin Documentation <https://docs.djangoproject.com/en/stable/ref/contrib/admin/>`_
* 🎨 `Admin Actions <https://docs.djangoproject.com/en/stable/ref/contrib/admin/actions/>`_
* 🔧 `Customizing Admin <https://docs.djangoproject.com/en/stable/intro/tutorial07/>`_

---

Django Admin is incredibly powerful for managing your application's data and users. With proper customization, it becomes an essential tool for both developers and content managers! 🎛️

Ready to learn about forms? Let's explore `Django Forms <./06-forms.rst>`_ next!