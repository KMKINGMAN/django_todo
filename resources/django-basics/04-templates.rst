========================
Django Templates Guide
========================

Templates in Django define how your data is presented to users. They separate the presentation layer from business logic, making your code more maintainable and allowing designers to work independently.

🎯 What are Django Templates?
=============================

Django templates are text files that define the structure and layout of your web pages. They can generate any text-based format (HTML, XML, CSV, etc.), but are most commonly used for HTML.

**Key Features:**

* 🎨 **Separation of Concerns**: Keep presentation separate from logic
* 🔄 **Template Inheritance**: Reuse common layouts
* 🧩 **Modular**: Include and extend templates
* 🛡️ **Auto-escaping**: Built-in XSS protection
* 🔧 **Flexible**: Custom tags and filters

🏗️ Template Syntax
==================

Django Template Language (DTL) uses a simple syntax:

Variables
---------

Display dynamic content using double curly braces:

.. code-block:: html

    <h1>{{ task.title }}</h1>
    <p>{{ task.description }}</p>
    <p>Created: {{ task.created_at|date:"Y-m-d" }}</p>

Tags
----

Control logic using curly braces with percent signs:

.. code-block:: html

    {% if task.completed %}
        <p class="completed">✅ Completed</p>
    {% else %}
        <p class="pending">⏳ Pending</p>
    {% endif %}

    {% for todo in todos %}
        <li>{{ todo.title }}</li>
    {% empty %}
        <li>No todos yet!</li>
    {% endfor %}

Comments
--------

.. code-block:: html

    {# This is a comment and won't be rendered #}
    
    {% comment %}
    This is a multi-line comment
    that can span several lines
    {% endcomment %}

📁 Template Directory Structure
==============================

Organize templates in a clear structure:

.. code-block:: text

    myproject/
    ├── templates/                    # Project-level templates
    │   ├── base.html                # Base template
    │   ├── 404.html                 # Error pages
    │   └── 500.html
    └── myapp/
        └── templates/
            └── myapp/               # App-specific templates
                ├── index.html
                ├── detail.html
                └── form.html

🎨 Template Inheritance
=======================

Base Template
-------------

Create a base template that other templates can extend:

.. code-block:: html

    <!-- templates/base.html -->
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{% block title %}Todo App{% endblock %}</title>
        
        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        
        {% block extra_css %}{% endblock %}
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand" href="{% url 'task_list' %}">📝 Todo App</a>
                
                <div class="navbar-nav ms-auto">
                    {% if user.is_authenticated %}
                        <span class="navbar-text me-3">Welcome, {{ user.username }}!</span>
                        <a class="nav-link" href="{% url 'logout' %}">Logout</a>
                    {% else %}
                        <a class="nav-link" href="{% url 'login' %}">Login</a>
                    {% endif %}
                </div>
            </div>
        </nav>

        <!-- Main content -->
        <main class="container mt-4">
            {% block content %}
            {% endblock %}
        </main>

        <!-- Footer -->
        <footer class="bg-light mt-5 py-4">
            <div class="container text-center">
                <p>&copy; 2023 Todo App. Built with Django.</p>
            </div>
        </footer>

        <!-- Bootstrap JS -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        {% block extra_js %}{% endblock %}
    </body>
    </html>

Child Template
--------------

Extend the base template and override specific blocks:

.. code-block:: html

    <!-- app/templates/app/task_list.html -->
    {% extends 'base.html' %}

    {% block title %}Tasks - Todo App{% endblock %}

    {% block content %}
    <div class="row">
        <div class="col-md-8">
            <h1>📋 My Tasks</h1>
            
            {% if tasks %}
                <div class="row">
                    {% for task in tasks %}
                    <div class="col-md-6 mb-3">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">{{ task.title }}</h5>
                                <p class="card-text">{{ task.description|truncatewords:15 }}</p>
                                
                                <div class="d-flex justify-content-between align-items-center">
                                    <small class="text-muted">
                                        Created {{ task.created_at|timesince }} ago
                                    </small>
                                    
                                    {% if task.completed %}
                                        <span class="badge bg-success">✅ Completed</span>
                                    {% else %}
                                        <span class="badge bg-warning">⏳ Pending</span>
                                    {% endif %}
                                </div>
                                
                                <div class="mt-2">
                                    <a href="{% url 'task_detail' task.id %}" class="btn btn-primary btn-sm">View</a>
                                    <a href="{% url 'task_edit' task.id %}" class="btn btn-outline-secondary btn-sm">Edit</a>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="alert alert-info">
                    <h4>No tasks yet!</h4>
                    <p>Create your first task to get started.</p>
                </div>
            {% endif %}
        </div>
        
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <h5>Quick Actions</h5>
                </div>
                <div class="card-body">
                    <a href="{% url 'task_create' %}" class="btn btn-success w-100 mb-2">
                        ➕ Create New Task
                    </a>
                    <a href="{% url 'completed_tasks' %}" class="btn btn-info w-100">
                        ✅ View Completed Tasks
                    </a>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}

🔧 Common Template Tags
=======================

Control Flow
------------

.. code-block:: html

    <!-- if/elif/else -->
    {% if task.priority == 'high' %}
        <span class="badge bg-danger">High Priority</span>
    {% elif task.priority == 'medium' %}
        <span class="badge bg-warning">Medium Priority</span>
    {% else %}
        <span class="badge bg-secondary">Low Priority</span>
    {% endif %}

    <!-- for loop -->
    {% for todo in task.todos.all %}
        <li class="{% if todo.completed %}completed{% endif %}">
            {{ todo.title }}
        </li>
    {% empty %}
        <li>No todos for this task</li>
    {% endfor %}

URL Generation
--------------

.. code-block:: html

    <!-- Named URL patterns -->
    <a href="{% url 'task_detail' task.id %}">View Task</a>
    <a href="{% url 'task_edit' task.id %}">Edit Task</a>

    <!-- URL with multiple parameters -->
    <a href="{% url 'todo_detail' task.id todo.id %}">View Todo</a>

Including Templates
-------------------

.. code-block:: html

    <!-- Include another template -->
    {% include 'app/task_card.html' with task=task %}

    <!-- Include with additional context -->
    {% include 'app/todo_list.html' with todos=task.todos.all show_task=False %}

Loading Static Files
--------------------

.. code-block:: html

    {% load static %}

    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    <script src="{% static 'js/app.js' %}"></script>
    <img src="{% static 'images/logo.png' %}" alt="Logo">

🎨 Template Filters
===================

Built-in Filters
----------------

.. code-block:: html

    <!-- String filters -->
    {{ task.title|upper }}                    <!-- UPPERCASE -->
    {{ task.title|lower }}                    <!-- lowercase -->
    {{ task.title|title }}                    <!-- Title Case -->
    {{ task.description|truncatewords:10 }}   <!-- Limit words -->
    {{ task.description|truncatechars:50 }}   <!-- Limit characters -->

    <!-- Date/time filters -->
    {{ task.created_at|date:"Y-m-d H:i" }}    <!-- Format date -->
    {{ task.created_at|timesince }}           <!-- "2 hours ago" -->
    {{ task.created_at|timeuntil }}           <!-- "in 3 days" -->

    <!-- Number filters -->
    {{ task.priority|add:1 }}                 <!-- Add numbers -->
    {{ price|floatformat:2 }}                 <!-- Format decimals -->

    <!-- List filters -->
    {{ todos|length }}                        <!-- Count items -->
    {{ todos|first }}                         <!-- First item -->
    {{ todos|last }}                          <!-- Last item -->
    {{ todos|slice:":5" }}                    <!-- First 5 items -->

    <!-- Default values -->
    {{ task.description|default:"No description" }}
    {{ task.due_date|default_if_none:"Not set" }}

Custom Filters
--------------

Create custom filters in ``templatetags/`` directory:

.. code-block:: python

    # app/templatetags/task_extras.py
    from django import template

    register = template.Library()

    @register.filter
    def priority_color(priority):
        """Return Bootstrap color class for priority."""
        colors = {
            'high': 'danger',
            'medium': 'warning',
            'low': 'secondary'
        }
        return colors.get(priority, 'secondary')

    @register.filter
    def completion_percentage(task):
        """Calculate completion percentage for a task."""
        total_todos = task.todos.count()
        if total_todos == 0:
            return 0
        completed_todos = task.todos.filter(completed=True).count()
        return round((completed_todos / total_todos) * 100)

Use custom filters in templates:

.. code-block:: html

    {% load task_extras %}

    <span class="badge bg-{{ task.priority|priority_color }}">
        {{ task.priority|title }}
    </span>

    <div class="progress">
        <div class="progress-bar" style="width: {{ task|completion_percentage }}%">
            {{ task|completion_percentage }}%
        </div>
    </div>

📋 Forms in Templates
=====================

Django forms integrate seamlessly with templates:

.. code-block:: html

    <!-- app/templates/app/task_form.html -->
    {% extends 'base.html' %}

    {% block title %}
        {% if form.instance.pk %}Edit Task{% else %}Create Task{% endif %} - Todo App
    {% endblock %}

    {% block content %}
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h4>
                        {% if form.instance.pk %}
                            ✏️ Edit Task
                        {% else %}
                            ➕ Create New Task
                        {% endif %}
                    </h4>
                </div>
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        
                        <!-- Manual form rendering -->
                        <div class="mb-3">
                            <label for="{{ form.title.id_for_label }}" class="form-label">
                                Title *
                            </label>
                            {{ form.title|add_class:"form-control" }}
                            {% if form.title.errors %}
                                <div class="text-danger">
                                    {{ form.title.errors }}
                                </div>
                            {% endif %}
                        </div>

                        <div class="mb-3">
                            <label for="{{ form.description.id_for_label }}" class="form-label">
                                Description
                            </label>
                            {{ form.description|add_class:"form-control" }}
                            {% if form.description.errors %}
                                <div class="text-danger">
                                    {{ form.description.errors }}
                                </div>
                            {% endif %}
                        </div>

                        <div class="mb-3 form-check">
                            {{ form.completed|add_class:"form-check-input" }}
                            <label for="{{ form.completed.id_for_label }}" class="form-check-label">
                                Mark as completed
                            </label>
                        </div>

                        <!-- Form buttons -->
                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                            <a href="{% url 'task_list' %}" class="btn btn-secondary">Cancel</a>
                            <button type="submit" class="btn btn-primary">
                                {% if form.instance.pk %}Update{% else %}Create{% endif %} Task
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}

🔧 Template Configuration
=========================

Settings
--------

Configure templates in ``settings.py``:

.. code-block:: python

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                BASE_DIR / 'templates',  # Project-level templates
            ],
            'APP_DIRS': True,  # Look for templates in app directories
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

Context Processors
------------------

Add data available to all templates:

.. code-block:: python

    # myapp/context_processors.py
    def site_info(request):
        """Add site-wide information to template context."""
        return {
            'site_name': 'Todo App',
            'current_year': datetime.now().year,
        }

    # settings.py
    TEMPLATES = [
        {
            # ... other settings
            'OPTIONS': {
                'context_processors': [
                    # ... default processors
                    'myapp.context_processors.site_info',
                ],
            },
        },
    ]

🎯 Our Todo App Templates
=========================

Task Detail Template
--------------------

.. code-block:: html

    <!-- app/templates/app/task_detail.html -->
    {% extends 'base.html' %}
    {% load task_extras %}

    {% block title %}{{ task.title }} - Todo App{% endblock %}

    {% block content %}
    <div class="row">
        <div class="col-md-8">
            <!-- Task Info -->
            <div class="card mb-4">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h3>{{ task.title }}</h3>
                    <span class="badge bg-{{ task.priority|priority_color }}">
                        {{ task.priority|title }} Priority
                    </span>
                </div>
                <div class="card-body">
                    <p class="card-text">{{ task.description|linebreaks }}</p>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <small class="text-muted">
                                Created: {{ task.created_at|date:"M d, Y" }}
                            </small>
                        </div>
                        <div class="col-md-6 text-end">
                            {% if task.completed %}
                                <span class="badge bg-success">✅ Completed</span>
                            {% else %}
                                <span class="badge bg-warning">⏳ In Progress</span>
                            {% endif %}
                        </div>
                    </div>
                </div>
                <div class="card-footer">
                    <a href="{% url 'task_edit' task.id %}" class="btn btn-primary">Edit Task</a>
                    <a href="{% url 'task_delete' task.id %}" class="btn btn-danger">Delete Task</a>
                </div>
            </div>

            <!-- Todos Section -->
            <div class="card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h4>📝 Todos ({{ task.todos.count }})</h4>
                    <div class="progress" style="width: 200px;">
                        <div class="progress-bar" 
                             style="width: {{ task|completion_percentage }}%">
                            {{ task|completion_percentage }}%
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    {% if task.todos.all %}
                        <ul class="list-group list-group-flush">
                            {% for todo in task.todos.all %}
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <div>
                                    <h6 class="{% if todo.completed %}text-decoration-line-through text-muted{% endif %}">
                                        {{ todo.title }}
                                    </h6>
                                    {% if todo.description %}
                                        <small class="text-muted">{{ todo.description }}</small>
                                    {% endif %}
                                </div>
                                <div>
                                    {% if todo.completed %}
                                        <span class="badge bg-success">✅</span>
                                    {% else %}
                                        <span class="badge bg-warning">⏳</span>
                                    {% endif %}
                                </div>
                            </li>
                            {% endfor %}
                        </ul>
                    {% else %}
                        <div class="text-center py-4">
                            <p class="text-muted">No todos yet for this task.</p>
                            <a href="{% url 'todo_create' task.id %}" class="btn btn-primary">
                                Add First Todo
                            </a>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>

        <div class="col-md-4">
            <!-- Quick Actions -->
            <div class="card">
                <div class="card-header">
                    <h5>Quick Actions</h5>
                </div>
                <div class="list-group list-group-flush">
                    <a href="{% url 'todo_create' task.id %}" class="list-group-item list-group-item-action">
                        ➕ Add Todo
                    </a>
                    <a href="{% url 'task_list' %}" class="list-group-item list-group-item-action">
                        📋 Back to Tasks
                    </a>
                    {% if not task.completed %}
                    <a href="{% url 'task_complete' task.id %}" class="list-group-item list-group-item-action">
                        ✅ Mark Complete
                    </a>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    {% endblock %}

🛡️ Template Security
====================

Auto-escaping
-------------

Django automatically escapes dangerous characters:

.. code-block:: html

    <!-- This is automatically escaped -->
    <p>{{ user_input }}</p>  <!-- <script> becomes &lt;script&gt; -->

    <!-- To disable escaping (use carefully!) -->
    <p>{{ trusted_html|safe }}</p>

    <!-- Mark content as safe in views -->
    from django.utils.safestring import mark_safe
    safe_content = mark_safe("<strong>Bold text</strong>")

CSRF Protection
---------------

Always include CSRF token in forms:

.. code-block:: html

    <form method="post">
        {% csrf_token %}
        <!-- form fields -->
    </form>

🧪 Testing Templates
====================

.. code-block:: python

    from django.test import TestCase
    from django.template import Template, Context
    from django.contrib.auth.models import User
    from .models import Task

    class TemplateTest(TestCase):
        def setUp(self):
            self.user = User.objects.create_user('testuser', 'test@example.com', 'pass')
            self.task = Task.objects.create(
                title='Test Task',
                description='Test Description',
                user=self.user
            )
        
        def test_template_rendering(self):
            """Test that template renders correctly."""
            response = self.client.get(f'/tasks/{self.task.id}/')
            self.assertContains(response, 'Test Task')
            self.assertContains(response, 'Test Description')
        
        def test_custom_filter(self):
            """Test custom template filter."""
            template = Template('{{ task|completion_percentage }}')
            context = Context({'task': self.task})
            rendered = template.render(context)
            self.assertEqual(rendered, '0')  # No todos yet

🎓 Best Practices
=================

1. **Keep Logic Out of Templates**
   - Move complex logic to views or model methods
   - Use template filters for simple formatting

2. **Use Template Inheritance**
   - Create a solid base template
   - Override only necessary blocks

3. **Organize Templates**
   - Use clear directory structure
   - Name templates descriptively

4. **Performance Considerations**
   - Minimize database queries in templates
   - Use ``select_related`` and ``prefetch_related`` in views

5. **Security First**
   - Never disable auto-escaping without good reason
   - Always use CSRF tokens in forms

📖 Next Steps
=============

1. 🔧 **Django Admin**: Learn about `Django Admin <./05-admin.rst>`_

🔗 Resources
============

* 📚 `Django Templates Documentation <https://docs.djangoproject.com/en/stable/topics/templates/>`_
* 🎨 `Template Language Reference <https://docs.djangoproject.com/en/stable/ref/templates/language/>`_
* 🔧 `Built-in Template Tags and Filters <https://docs.djangoproject.com/en/stable/ref/templates/builtins/>`_

---

Templates are where your data comes to life! With Django's powerful template system, you can create beautiful, dynamic web pages that are both maintainable and secure. 🎨

Ready to make administration easy? Let's explore `Django Admin <./05-admin.rst>`_ next!