======================================
Todo Application Architecture
======================================

This document provides a comprehensive overview of the Django Todo Application architecture, explaining how all components work together to create a full-stack task management system.

🏗️ System Overview
==================

The Todo Application is a full-stack web application built with:

* **Backend**: Django + Django REST Framework
* **Frontend**: React + Material-UI
* **Database**: SQLite (easily configurable to PostgreSQL/MySQL)
* **Authentication**: Token-based authentication
* **API**: RESTful API design

📊 High-Level Architecture
==========================

.. code-block:: text

    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │   React Client  │    │  Django Backend │    │    Database     │
    │                 │    │                 │    │                 │
    │  • Material-UI  │◄──►│  • REST API     │◄──►│   • SQLite      │
    │  • Axios        │    │  • Authentication│    │   • Tasks       │
    │  • Router       │    │  • Business Logic│    │   • Todos       │
    └─────────────────┘    └─────────────────┘    └─────────────────┘

🗃️ Database Schema
==================

Entity Relationship Diagram
---------------------------

.. code-block:: text

    ┌─────────────────┐
    │      User       │
    │                 │
    │ • id            │
    │ • username      │
    │ • email         │
    │ • password      │
    └─────────┬───────┘
              │
              │ 1:N
              │
    ┌─────────▼───────┐    ┌─────────────────┐
    │      Task       │    │      Todo       │
    │                 │    │                 │
    │ • id            │◄───┤ • id            │
    │ • title         │1:N │ • title         │
    │ • description   │    │ • description   │
    │ • created_at    │    │ • completed     │
    │ • updated_at    │    │ • created_at    │
    │ • user_id (FK)  │    │ • updated_at    │
    └─────────────────┘    │ • due_date      │
                           │ • tags (JSON)   │
                           │ • user_id (FK)  │
                           │ • task_id (FK)  │
                           └─────────────────┘

Model Relationships
-------------------

1. **User → Task**: One-to-Many
   - One user can have multiple tasks
   - Each task belongs to exactly one user

2. **User → Todo**: One-to-Many
   - One user can have multiple todos
   - Each todo belongs to exactly one user

3. **Task → Todo**: One-to-Many (Optional)
   - One task can have multiple todos
   - Todos can exist without a task (standalone todos)

🔧 Backend Architecture
=======================

Django Project Structure
------------------------

.. code-block:: text

    backend/
    ├── manage.py                    # Django command-line utility
    ├── db.sqlite3                   # Database file
    ├── requirements.txt             # Python dependencies
    ├── .pylintrc                    # Code quality configuration
    ├── todo_application/            # Project configuration
    │   ├── __init__.py
    │   ├── settings.py              # Django settings
    │   ├── urls.py                  # Main URL routing
    │   ├── wsgi.py                  # WSGI configuration
    │   └── asgi.py                  # ASGI configuration
    ├── app/                         # Main application
    │   ├── models/                  # Data models
    │   │   ├── __init__.py
    │   │   ├── task_model.py        # Task model definition
    │   │   └── todo_model.py        # Todo model definition
    │   ├── serializers/             # API serializers
    │   │   ├── __init__.py
    │   │   ├── task_serializer.py   # Task API serialization
    │   │   └── todo_serializer.py   # Todo API serialization
    │   ├── views/                   # API views
    │   │   ├── __init__.py
    │   │   ├── task_view.py         # Task API endpoints
    │   │   ├── todo_view.py         # Todo API endpoints
    │   │   └── auth_view.py         # Authentication endpoints
    │   ├── migrations/              # Database migrations
    │   ├── admin.py                 # Django admin configuration
    │   ├── apps.py                  # App configuration
    │   ├── tests.py                 # Basic tests
    │   └── urls.py                  # App URL routing
    ├── templates/                   # HTML templates
    │   ├── base.html                # Base template
    │   ├── dashboard.html           # Dashboard page
    │   └── registration/
    │       └── login.html           # Login page
    └── tests/                       # Comprehensive test suite
        ├── conftest.py              # Test configuration
        ├── factories.py             # Test data factories
        ├── test_models.py           # Model tests
        ├── test_task_api.py         # Task API tests
        ├── test_todo_api.py         # Todo API tests
        ├── test_auth_api.py         # Authentication tests
        └── test_integration.py      # Integration tests

API Design
----------

RESTful Endpoints
~~~~~~~~~~~~~~~~~

**Task Endpoints:**

.. code-block:: text

    GET    /api/tasks/              # List user's tasks
    POST   /api/tasks/              # Create new task
    GET    /api/tasks/{id}/         # Get specific task
    PUT    /api/tasks/{id}/         # Update entire task
    PATCH  /api/tasks/{id}/         # Partial update task
    DELETE /api/tasks/{id}/         # Delete task
    GET    /api/tasks/{id}/todos/   # Get todos for specific task

**Todo Endpoints:**

.. code-block:: text

    GET    /api/todos/              # List user's todos
    POST   /api/todos/              # Create new todo
    GET    /api/todos/{id}/         # Get specific todo
    PUT    /api/todos/{id}/         # Update entire todo
    PATCH  /api/todos/{id}/         # Partial update todo
    DELETE /api/todos/{id}/         # Delete todo
    POST   /api/todos/{id}/toggle_complete/  # Toggle completion status

**Authentication Endpoints:**

.. code-block:: text

    POST   /api/auth/login/         # User login (returns token)
    POST   /logout/                 # User logout

🎨 Frontend Architecture
========================

React Application Structure
---------------------------

.. code-block:: text

    frontend/
    ├── package.json                 # Dependencies and scripts
    ├── public/                      # Static files
    │   ├── index.html               # HTML template
    │   ├── favicon.ico              # App icon
    │   └── manifest.json            # PWA manifest
    ├── src/                         # Source code
    │   ├── index.js                 # Application entry point
    │   ├── App.js                   # Main application component
    │   ├── App.css                  # Global styles
    │   ├── components/              # Reusable UI components
    │   │   ├── TaskList.js          # Task list component
    │   │   ├── TodoList.js          # Todo list component
    │   │   ├── TaskDetailView.js    # Task detail view
    │   │   ├── LoginPage.js         # Login form
    │   │   └── DashboardPage.js     # Main dashboard
    │   ├── services/                # API services
    │   │   └── api.js               # Axios API client
    │   └── utils/                   # Utility functions
    └── build/                       # Production build (generated)

Component Hierarchy
-------------------

.. code-block:: text

    App
    ├── Router
        ├── LoginPage
        └── DashboardPage
            ├── TaskList
            │   └── TaskDetailView
            │       └── TodoList
            └── Navigation

State Management
---------------

The application uses React's built-in state management:

* **Local State**: Component-level state for UI interactions
* **Lifted State**: Shared state moved to parent components
* **Context**: Authentication state shared across components

.. code-block:: javascript

    // Authentication Context
    const AuthContext = createContext();

    export const AuthProvider = ({ children }) => {
      const [user, setUser] = useState(null);
      const [token, setToken] = useState(localStorage.getItem('token'));
      
      return (
        <AuthContext.Provider value={{ user, token, setUser, setToken }}>
          {children}
        </AuthContext.Provider>
      );
    };

🔄 Data Flow
============

1. User Authentication Flow
---------------------------

.. code-block:: text

    1. User enters credentials → LoginPage
    2. LoginPage calls API → /api/auth/login/
    3. Backend validates → Returns token + user info
    4. Frontend stores token → localStorage
    5. Frontend redirects → Dashboard
    6. All subsequent API calls → Include Authorization header

2. Task Management Flow
-----------------------

.. code-block:: text

    1. User creates task → TaskList component
    2. Component calls API → POST /api/tasks/
    3. Backend creates task → Associates with user
    4. Backend returns data → New task object
    5. Frontend updates state → Refreshes task list
    6. User sees new task → Immediately in UI

3. Todo Operations Flow
-----------------------

.. code-block:: text

    1. User toggles todo → TodoList component
    2. Component calls API → POST /api/todos/{id}/toggle_complete/
    3. Backend updates status → Saves to database
    4. Backend returns new status → { completed: true }
    5. Frontend updates state → Updates checkbox
    6. UI reflects change → Immediate feedback

🔐 Security Architecture
========================

Authentication
--------------

* **Token-based**: Django REST Framework Token Authentication
* **Stateless**: No server-side session storage
* **Secure Storage**: Tokens stored in localStorage (consider httpOnly cookies for production)

Authorization
-------------

* **User Isolation**: Users can only access their own data
* **Queryset Filtering**: All API views filter by ``request.user``
* **Permission Classes**: ``IsAuthenticated`` required for all API endpoints

CORS Configuration
------------------

.. code-block:: python

    # settings.py
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",  # React development server
        "http://127.0.0.1:3000",
    ]

    CORS_ALLOW_CREDENTIALS = True

🧪 Testing Strategy
==================

Backend Testing
---------------

1. **Model Tests**: Validate model behavior and relationships
2. **API Tests**: Test all endpoints with various scenarios
3. **Authentication Tests**: Verify security and permissions
4. **Integration Tests**: Test complete workflows

Test Coverage Areas
-------------------

* ✅ User authentication and authorization
* ✅ CRUD operations for tasks and todos
* ✅ Data validation and error handling
* ✅ User data isolation
* ✅ Edge cases and error conditions

Testing Tools
-------------

* **Django TestCase**: For model and basic view tests
* **DRF APITestCase**: For API endpoint testing
* **Factory Boy**: For generating test data
* **Pytest**: For advanced testing features

🚀 Deployment Architecture
==========================

Production Setup
----------------

.. code-block:: text

    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │   Nginx         │    │   Django App    │    │   PostgreSQL    │
    │   (Static Files)│    │   (Gunicorn)    │    │   (Database)    │
    │   (Reverse      │◄──►│                 │◄──►│                 │
    │    Proxy)       │    │                 │    │                 │
    └─────────────────┘    └─────────────────┘    └─────────────────┘

Environment Configuration
-------------------------

.. code-block:: python

    # Production settings
    DEBUG = False
    ALLOWED_HOSTS = ['yourdomain.com']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT'),
        }
    }

🔗 Resources
============

* 📚 `Django Documentation <https://docs.djangoproject.com/>`_
* 🚀 `Django REST Framework <https://www.django-rest-framework.org/>`_
* ⚛️ `React Documentation <https://reactjs.org/docs/>`_
* 🎨 `Material-UI <https://mui.com/>`_

---

This architecture provides a solid foundation for a modern, scalable web application with clear separation of concerns and robust security practices! 🏗️