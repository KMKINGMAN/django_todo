==============================
Django Models - Your Data Layer
==============================

Models are the heart of Django applications. They define your data structure, handle database operations, and contain business logic. Think of models as the blueprint for your database tables.

🎯 What are Models?
===================

A Django model is a Python class that represents a database table. Each model attribute corresponds to a database field.

.. code-block:: python

    from django.db import models

    class Task(models.Model):
        title = models.CharField(max_length=200)
        description = models.TextField(blank=True)
        created_at = models.DateTimeField(auto_now_add=True)
        completed = models.BooleanField(default=False)

This creates a database table with four columns: ``title``, ``description``, ``created_at``, and ``completed``.

📊 Field Types
==============

Django provides many field types for different data:

Text Fields
-----------

.. code-block:: python

    class MyModel(models.Model):
        # Short text (max 255 chars)
        title = models.CharField(max_length=100)
        
        # Long text
        description = models.TextField()
        
        # Email validation
        email = models.EmailField()
        
        # URL validation
        website = models.URLField()
        
        # Choices
        STATUS_CHOICES = [
            ('draft', 'Draft'),
            ('published', 'Published'),
        ]
        status = models.CharField(max_length=10, choices=STATUS_CHOICES)

Numeric Fields
--------------

.. code-block:: python

    class Product(models.Model):
        # Integers
        quantity = models.IntegerField()
        
        # Positive integers only
        rating = models.PositiveIntegerField()
        
        # Decimals for money
        price = models.DecimalField(max_digits=10, decimal_places=2)
        
        # Floating point numbers
        weight = models.FloatField()

Date and Time Fields
--------------------

.. code-block:: python

    class Event(models.Model):
        # Date only
        event_date = models.DateField()
        
        # Time only
        start_time = models.TimeField()
        
        # Date and time
        created_at = models.DateTimeField(auto_now_add=True)  # Set on creation
        updated_at = models.DateTimeField(auto_now=True)     # Updated on save

Boolean and File Fields
-----------------------

.. code-block:: python

    class Article(models.Model):
        # True/False
        is_published = models.BooleanField(default=False)
        
        # File upload
        document = models.FileField(upload_to='documents/')
        
        # Image upload (requires Pillow)
        thumbnail = models.ImageField(upload_to='images/')

🔗 Relationships
================

Models can be related to each other in three ways:

One-to-Many (ForeignKey)
------------------------

.. code-block:: python

    class User(models.Model):
        username = models.CharField(max_length=50)
        email = models.EmailField()

    class Task(models.Model):
        title = models.CharField(max_length=200)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        
    # One user can have many tasks
    # user.task_set.all() - gets all tasks for a user

Many-to-Many
------------

.. code-block:: python

    class Tag(models.Model):
        name = models.CharField(max_length=50)

    class Task(models.Model):
        title = models.CharField(max_length=200)
        tags = models.ManyToManyField(Tag, blank=True)
        
    # Many tasks can have many tags
    # task.tags.all() - gets all tags for a task
    # tag.task_set.all() - gets all tasks with this tag

One-to-One
----------

.. code-block:: python

    class User(models.Model):
        username = models.CharField(max_length=50)

    class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        bio = models.TextField()
        
    # Each user has exactly one profile
    # user.profile - gets the profile

🎯 Our Todo App Models
======================

Let's look at the models in our todo application:

Task Model
----------

.. code-block:: python

    class Task(models.Model):
        title = models.CharField(max_length=200)
        description = models.TextField(blank=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        user = models.ForeignKey(User, on_delete=models.CASCADE)

        class Meta:
            ordering = ['-created_at']  # Newest first

        def __str__(self):
            return self.title

Todo Model
----------

.. code-block:: python

    class Todo(models.Model):
        title = models.CharField(max_length=200)
        description = models.TextField(blank=True)
        completed = models.BooleanField(default=False)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        due_date = models.DateTimeField(null=True, blank=True)
        tags = models.JSONField(default=list, blank=True)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)

        class Meta:
            ordering = ['-created_at']

        def __str__(self):
            return self.title

🎨 Model Methods and Properties
===============================

Add custom methods to your models:

.. code-block:: python

    class Task(models.Model):
        title = models.CharField(max_length=200)
        created_at = models.DateTimeField(auto_now_add=True)
        
        def __str__(self):
            """String representation of the model."""
            return self.title
        
        def get_absolute_url(self):
            """URL for this object."""
            from django.urls import reverse
            return reverse('task-detail', args=[str(self.id)])
        
        @property
        def is_recent(self):
            """Check if task was created recently."""
            from django.utils import timezone
            return self.created_at >= timezone.now() - timezone.timedelta(days=1)
        
        def get_todo_count(self):
            """Get number of todos for this task."""
            return self.todo_set.count()

🔧 Model Meta Options
=====================

The ``Meta`` class provides model metadata:

.. code-block:: python

    class Task(models.Model):
        title = models.CharField(max_length=200)
        created_at = models.DateTimeField(auto_now_add=True)
        
        class Meta:
            # Database table name
            db_table = 'tasks'
            
            # Default ordering
            ordering = ['-created_at', 'title']
            
            # Unique constraints
            unique_together = ['title', 'user']
            
            # Human-readable names
            verbose_name = 'Task'
            verbose_name_plural = 'Tasks'
            
            # Permissions
            permissions = [
                ('can_publish', 'Can publish tasks'),
            ]

🗃️ Database Operations (ORM)
============================

Django's ORM (Object-Relational Mapping) lets you interact with the database using Python:

Creating Objects
----------------

.. code-block:: python

    # Method 1: Create and save
    task = Task(title="Learn Django", description="Study models")
    task.save()

    # Method 2: Create in one step
    task = Task.objects.create(
        title="Learn Django",
        description="Study models"
    )

    # Method 3: Get or create
    task, created = Task.objects.get_or_create(
        title="Learn Django",
        defaults={'description': 'Study models'}
    )

Querying Objects
----------------

.. code-block:: python

    # Get all objects
    all_tasks = Task.objects.all()

    # Filter objects
    completed_tasks = Task.objects.filter(completed=True)
    recent_tasks = Task.objects.filter(created_at__gte=yesterday)

    # Get single object
    task = Task.objects.get(id=1)
    task = Task.objects.get(title="Learn Django")

    # First/last object
    first_task = Task.objects.first()
    latest_task = Task.objects.latest('created_at')

    # Check if exists
    exists = Task.objects.filter(title="Learn Django").exists()

    # Count objects
    count = Task.objects.count()

Complex Queries
---------------

.. code-block:: python

    from django.db.models import Q

    # OR conditions
    tasks = Task.objects.filter(
        Q(title__icontains="django") | Q(description__icontains="django")
    )

    # Exclude
    tasks = Task.objects.exclude(completed=True)

    # Related object filtering
    tasks_with_todos = Task.objects.filter(todo__isnull=False).distinct()

    # Ordering
    tasks = Task.objects.order_by('-created_at', 'title')

    # Limiting results
    latest_5_tasks = Task.objects.all()[:5]

Updating Objects
----------------

.. code-block:: python

    # Update single object
    task = Task.objects.get(id=1)
    task.title = "Updated Title"
    task.save()

    # Update multiple objects
    Task.objects.filter(completed=False).update(completed=True)

    # Update or create
    task, created = Task.objects.update_or_create(
        id=1,
        defaults={'title': 'Updated Title'}
    )

Deleting Objects
----------------

.. code-block:: python

    # Delete single object
    task = Task.objects.get(id=1)
    task.delete()

    # Delete multiple objects
    Task.objects.filter(completed=True).delete()

    # Delete all objects (be careful!)
    Task.objects.all().delete()

🔄 Migrations
=============

When you change models, create and apply migrations:

.. code-block:: bash

    # Create migrations for changes
    python manage.py makemigrations

    # Apply migrations to database
    python manage.py migrate

    # View migration SQL
    python manage.py sqlmigrate app_name 0001

    # Show migration status
    python manage.py showmigrations

🎓 Best Practices
=================

1. Always Use ``__str__`` Method
--------------------------------

.. code-block:: python

    class Task(models.Model):
        title = models.CharField(max_length=200)
        
        def __str__(self):
            return self.title  # Shows meaningful name in admin

2. Use Appropriate Field Options
--------------------------------

.. code-block:: python

    class Task(models.Model):
        title = models.CharField(max_length=200)
        description = models.TextField(blank=True)  # Optional field
        email = models.EmailField(unique=True)      # Unique constraint
        created_at = models.DateTimeField(auto_now_add=True)  # Set once
        updated_at = models.DateTimeField(auto_now=True)      # Updates on save

3. Use Related Names for Clarity
--------------------------------

.. code-block:: python

    class User(models.Model):
        username = models.CharField(max_length=50)

    class Task(models.Model):
        title = models.CharField(max_length=200)
        user = models.ForeignKey(
            User, 
            on_delete=models.CASCADE,
            related_name='tasks'  # Now use user.tasks.all()
        )

4. Be Careful with Cascade Deletions
------------------------------------

.. code-block:: python

    class Task(models.Model):
        user = models.ForeignKey(
            User, 
            on_delete=models.CASCADE    # Delete tasks when user is deleted
        )

    class Profile(models.Model):
        user = models.OneToOneField(
            User,
            on_delete=models.PROTECT    # Prevent user deletion if profile exists
        )

🧪 Testing Models
=================

.. code-block:: python

    from django.test import TestCase
    from django.contrib.auth.models import User
    from .models import Task

    class TaskModelTest(TestCase):
        def setUp(self):
            self.user = User.objects.create_user(
                username='testuser',
                password='testpass123'
            )
        
        def test_task_creation(self):
            task = Task.objects.create(
                title='Test Task',
                user=self.user
            )
            self.assertEqual(task.title, 'Test Task')
            self.assertEqual(str(task), 'Test Task')
        
        def test_task_is_recent(self):
            task = Task.objects.create(
                title='Recent Task',
                user=self.user
            )
            self.assertTrue(task.is_recent)

📖 Next Steps
=============

1. 👀 **Learn Views**: Understand how to `work with models in views <./03-views-urls.rst>`_
2. 🎨 **Templates**: Display model data in `templates <./04-templates.rst>`_
3. 🔧 **Admin**: Manage models through `Django Admin <./05-admin.rst>`_

🔗 Further Reading
==================

* 📚 `Model Field Reference <https://docs.djangoproject.com/en/stable/ref/models/fields/>`_
* 🔍 `QuerySet API <https://docs.djangoproject.com/en/stable/ref/models/querysets/>`_
* 📊 `Database Optimization <https://docs.djangoproject.com/en/stable/topics/db/optimization/>`_

---

Models are the foundation of your Django application. Master them well, and you'll have a solid base for building powerful web applications! 🚀

Ready to learn how views interact with models? Let's explore `Views and URLs <./03-views-urls.rst>`_!