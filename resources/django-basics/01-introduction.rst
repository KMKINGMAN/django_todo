=============================
Django Introduction
=============================

Welcome to Django! This guide will introduce you to Django's core concepts and help you understand how web applications are built with this powerful Python framework.

🎯 What is Django?
==================

Django is a high-level Python web framework that enables rapid development of secure and maintainable websites. It follows the **"Don't Repeat Yourself" (DRY)** principle and uses a **Model-View-Template (MVT)** architecture.

Key Features
------------

* 🚀 **Rapid Development**: Build applications quickly with minimal code
* 🔒 **Security**: Built-in protection against common web vulnerabilities
* 📈 **Scalable**: Powers sites from small blogs to large-scale applications
* 🧩 **Modular**: Reusable apps and components
* 🗃️ **ORM**: Object-Relational Mapping for database interactions

🏗️ Django Architecture (MVT Pattern)
=====================================

Django uses the **Model-View-Template** pattern:

.. code-block:: text

    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │    Model    │    │     View    │    │  Template   │
    │             │    │             │    │             │
    │ Data Layer  │◄──►│ Logic Layer │◄──►│ Presentation│
    │ (Database)  │    │ (Python)    │    │    (HTML)   │
    └─────────────┘    └─────────────┘    └─────────────┘

📊 Model (Data Layer)
---------------------

* Defines your data structure
* Handles database operations
* Contains business logic

🧠 View (Logic Layer)
---------------------

* Processes HTTP requests
* Contains application logic
* Returns HTTP responses

🎨 Template (Presentation Layer)
--------------------------------

* Defines how data is displayed
* HTML with Django template language
* Dynamic content rendering

🚀 Getting Started
==================

Basic Django Workflow
----------------------

1. **URL Request** → User visits a URL
2. **URL Routing** → Django matches URL to a view
3. **View Processing** → View processes the request
4. **Model Interaction** → View queries/updates database via models
5. **Template Rendering** → View renders template with data
6. **HTTP Response** → Rendered page sent to user

Project Structure
-----------------

.. code-block:: text

    myproject/
    ├── manage.py              # Command-line utility
    ├── myproject/            # Project configuration
    │   ├── __init__.py
    │   ├── settings.py       # Project settings
    │   ├── urls.py           # URL routing
    │   └── wsgi.py           # WSGI configuration
    └── myapp/                # Django app
        ├── __init__.py
        ├── admin.py          # Admin interface
        ├── apps.py           # App configuration
        ├── models.py         # Data models
        ├── views.py          # View functions
        ├── urls.py           # App URL patterns
        ├── tests.py          # Tests
        └── migrations/       # Database migrations

📚 Core Concepts
================

🏢 Projects vs Apps
-------------------

**Project**: The entire Django application

* Contains settings, URL configuration
* Can contain multiple apps

**App**: A specific functionality module

* Models, views, templates for specific feature
* Reusable across projects

🗃️ Models
---------

Models define your data structure and database schema:

.. code-block:: python

    from django.db import models

    class Task(models.Model):
        title = models.CharField(max_length=200)
        description = models.TextField(blank=True)
        created_at = models.DateTimeField(auto_now_add=True)
        completed = models.BooleanField(default=False)
        
        def __str__(self):
            return self.title

🔗 URLs
-------

URL patterns map URLs to views:

.. code-block:: python

    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.index, name='index'),
        path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    ]

👀 Views
--------

Views handle HTTP requests and return responses:

.. code-block:: python

    from django.shortcuts import render
    from .models import Task

    def index(request):
        tasks = Task.objects.all()
        return render(request, 'tasks/index.html', {'tasks': tasks})

    def task_detail(request, task_id):
        task = Task.objects.get(id=task_id)
        return render(request, 'tasks/detail.html', {'task': task})

🛠️ Essential Commands
=====================

Project Setup
--------------

.. code-block:: bash

    # Create new project
    django-admin startproject myproject

    # Create new app
    python manage.py startapp myapp

    # Development server
    python manage.py runserver

Database Operations
-------------------

.. code-block:: bash

    # Create migrations
    python manage.py makemigrations

    # Apply migrations
    python manage.py migrate

    # Create superuser
    python manage.py createsuperuser

Other Useful Commands
---------------------

.. code-block:: bash

    # Django shell
    python manage.py shell

    # Collect static files
    python manage.py collectstatic

    # Run tests
    python manage.py test

🔧 Key Settings
===============

Django settings are configured in ``settings.py``:

.. code-block:: python

    # Essential settings
    DEBUG = True  # Never True in production
    ALLOWED_HOSTS = []

    # Database configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    # Installed apps
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'myapp',  # Your custom app
    ]

🎓 Learning Path
================

Beginner Level
--------------

1. ✅ Understand MVT pattern
2. ✅ Create simple models
3. ✅ Write basic views
4. ✅ Set up URL routing
5. ✅ Use Django admin

Intermediate Level
------------------

1. 📝 Forms and form handling
2. 🔐 User authentication
3. 🎨 Template inheritance
4. 🗃️ Complex model relationships
5. 🧪 Testing

Advanced Level
--------------

1. 🚀 Custom middleware
2. 📧 Email and notifications
3. 🔒 Advanced security
4. 📊 Performance optimization
5. 🌐 API development (Django REST Framework)

📖 Next Steps
=============

1. 📊 **Learn Models**: Dive deep into `Django Models <./02-models.rst>`_
2. 👀 **Understand Views**: Explore `Views and URLs <./03-views-urls.rst>`_
3. 🎨 **Template Basics**: Check `Templates <./04-templates.rst>`_
4. 🔧 **Admin Interface**: Set up `Django Admin <./05-admin.rst>`_

🔗 Official Resources
=====================

* 📚 `Django Documentation <https://docs.djangoproject.com/>`_
* 🎓 `Django Tutorial <https://docs.djangoproject.com/en/stable/intro/tutorial01/>`_
* 📖 `Django Best Practices <https://django-best-practices.readthedocs.io/>`_

.. note::
   Django is designed to make development fast and enjoyable. Don't worry about memorizing everything - the documentation is excellent and the community is helpful!

Ready to dive deeper? Let's explore `Django Models <./02-models.rst>`_ next! 🚀