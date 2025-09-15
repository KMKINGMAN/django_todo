Todo api
==================

A Django REST Framework-based Todo application with authentication and a web dashboard for training.

Features
--------

* todo 

Installation
------------

1. Install dependencies::

    pip install -r requirements.txt

2. Run migrations::

    python manage.py migrate

3. Create a superuser (optional)::

    python manage.py createsuperuser

4. Run the development server::

    python manage.py runserver

API Endpoints
-------------

All API endpoints require authentication.

**Base URL:** ``/api/``

**Todo Operations:**

* ``GET /api/todos/`` - List all todos for authenticated user
* ``POST /api/todos/`` - Create a new todo
* ``GET /api/todos/{id}/`` - Retrieve a specific todo
* ``PUT /api/todos/{id}/`` - Update a todo completely
* ``PATCH /api/todos/{id}/`` - Partially update a todo
* ``DELETE /api/todos/{id}/`` - Delete a todo

**Todo Fields:**

.. code-block:: javascript

    {
        "id": 1,
        "title": "Meeting with CTO Mr.Omar",
        "description": "Discuss new features in openEdx platform",
        "completed": false,
        "due_date": "2025-09-15T10:00:00Z",
        "created_at": "2025-09-13T14:30:00Z",
        "updated_at": "2025-09-13T14:30:00Z",
        "tags": ["development", "urgent"],
        "user": [1]
    }

Authentication
--------------

**Web Interface:**
- Login: ``/accounts/login/``
- Logout: ``/accounts/logout/``
- Dashboard: ``/dashboard/``

**API Authentication:**
- Session authentication (for web dashboard)
- Token authentication can be added for mobile/external clients

Usage Examples
--------------

**Create a todo:**

.. code-block:: 

    curl -X POST http://localhost:8000/api/todos/ \
         -H "Content-Type: application/json" \
         -H "X-CSRFToken: YOUR_CSRF_TOKEN" \
         -d '{"title": "Learn Django", "tags": ["programming"]}'

**Update completion status:**

.. code-block:: 

    curl -X PATCH http://localhost:8000/api/todos/1/ \
         -H "Content-Type: application/json" \
         -H "X-CSRFToken: YOUR_CSRF_TOKEN" \
         -d '{"completed": true}'

Testing
-------

Run the test suite::

    python manage.py test

Development
-----------

**Admin Interface:**
Access at ``/admin/`` to manage todos, users, and other data.

**Dashboard:**
Web interface at ``/dashboard/`` provides a user-friendly way to manage todos
with create, read, update, and delete functionality.
