=======================================
Django Todo Application
=======================================

A full-stack task management application built with Django, Django REST Framework, and React. This project demonstrates modern web development practices including RESTful API design, token authentication, and responsive UI components.

🚀 Quick Start
==============

**For Beginners:**

1. 📚 **New to Django?** → Start with our `Django Basics Guide <./resources/django-basics/01-introduction.rst>`_
2. 🔧 **New to APIs?** → Learn `Django REST Framework <./resources/django-rest-framework/01-introduction.rst>`_
3. 🏗️ **Understanding this app?** → Check `Project Architecture <./resources/project-documentation/architecture.rst>`_

**For Developers:**

.. code-block:: bash

    # Backend setup
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

    # Frontend setup (in another terminal)
    cd frontend
    npm install
    npm start

    # Access the application
    # Frontend: http://localhost:3000
    # Backend API: http://localhost:8000/api/
    # Admin Panel: http://localhost:8000/admin/

✨ Features
===========

🎯 **Core Functionality**
-------------------------

* ✅ **Task Management**: Create, edit, delete, and organize tasks
* 📝 **Todo Lists**: Add todos to tasks or create standalone todos
* ✔️ **Completion Tracking**: Mark tasks and todos as complete
* 🏷️ **Tagging System**: Organize todos with custom tags
* 📅 **Due Dates**: Set and track deadlines
* 👤 **User Accounts**: Personal task management with secure authentication

🛡️ **Security Features**
------------------------

* 🔐 **Token Authentication**: Secure API access with JWT-like tokens
* 🔒 **User Isolation**: Users can only access their own data
* 🛡️ **CORS Protection**: Properly configured cross-origin requests
* 🔍 **Input Validation**: Comprehensive data validation on all endpoints

🎨 **User Experience**
---------------------

* 📱 **Responsive Design**: Works on desktop, tablet, and mobile
* 🌙 **Dark Theme**: Modern Material-UI dark theme
* ⚡ **Real-time Updates**: Instant UI feedback for all actions
* 🔄 **Optimistic Updates**: UI updates immediately, syncs with server
* 🚪 **Easy Authentication**: Simple login/logout flow

🏗️ **Technical Excellence**
---------------------------

* 📊 **RESTful API**: Clean, predictable API endpoints
* 🧪 **Comprehensive Testing**: 95%+ test coverage
* 📝 **Code Quality**: Pylint integration with high standards
* 📚 **Documentation**: Extensive learning resources
* 🔧 **Maintainable Code**: Well-organized, modular architecture

🏗️ Architecture Overview
========================

System Components
-----------------

.. code-block:: text

    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │   React Client  │    │  Django Backend │    │    Database     │
    │                 │    │                 │    │                 │
    │  • Material-UI  │◄──►│  • REST API     │◄──►│   • SQLite      │
    │  • Axios        │    │  • Authentication│    │   • Tasks       │
    │  • Router       │    │  • Business Logic│    │   • Todos       │
    └─────────────────┘    └─────────────────┘    └─────────────────┘

**Backend (Django + DRF)**

* 🗃️ **Models**: Task and Todo models with user relationships
* 🔗 **API**: RESTful endpoints using ViewSets and Serializers
* 🔐 **Auth**: Token-based authentication system
* 🧪 **Tests**: Comprehensive test suite with factories

**Frontend (React + Material-UI)**

* ⚛️ **Components**: Modular, reusable UI components
* 🎨 **Styling**: Material-UI dark theme with responsive design
* 📡 **API Client**: Axios for HTTP requests with token auth
* 🔄 **State**: React hooks and context for state management

**Database Schema**

.. code-block:: text

    User (Django Auth)
    ├── Task (1:N)
    │   ├── id, title, description
    │   ├── created_at, updated_at
    │   └── user_id (FK)
    └── Todo (1:N)
        ├── id, title, description
        ├── completed, due_date, tags
        ├── created_at, updated_at
        ├── user_id (FK)
        └── task_id (FK, optional)

📂 Project Structure
===================

.. code-block:: text

    django_application/
    ├── 📁 backend/                 # Django backend
    │   ├── 📁 app/                 # Main application
    │   │   ├── 📁 models/          # Data models
    │   │   ├── 📁 serializers/     # API serializers
    │   │   ├── 📁 views/           # API views
    │   │   └── 📁 migrations/      # Database migrations
    │   ├── 📁 tests/               # Test suite
    │   ├── 📁 templates/           # HTML templates
    │   ├── 📄 manage.py            # Django CLI
    │   └── 📄 requirements.txt     # Python dependencies
    ├── 📁 frontend/                # React frontend
    │   ├── 📁 src/                 # Source code
    │   │   ├── 📁 components/      # React components
    │   │   └── 📁 services/        # API services
    │   ├── 📁 public/              # Static files
    │   └── 📄 package.json         # Node dependencies
    └── 📁 resources/               # Learning materials
        ├── 📁 django-basics/       # Django fundamentals
        ├── 📁 django-rest-framework/  # DRF guides
        └── 📁 project-documentation/  # This app's docs

🎓 Learning Resources
====================

We've created comprehensive learning materials for developers at all levels:

📚 **Django Fundamentals**
--------------------------

Perfect for beginners or those wanting to refresh their Django knowledge:

* `🎯 Django Introduction <./resources/django-basics/01-introduction.rst>`_ - Core concepts and MVT pattern
* `🗃️ Django Models <./resources/django-basics/02-models.rst>`_ - Database modeling and ORM
* `👀 Views & URLs <./resources/django-basics/03-views-urls.rst>`_ - Request handling and routing
* `🎨 Templates <./resources/django-basics/04-templates.rst>`_ - Dynamic HTML generation
* `🔧 Django Admin <./resources/django-basics/05-admin.rst>`_ - Built-in administration interface

🚀 **Django REST Framework**
----------------------------

Learn modern API development with DRF:

* `📡 DRF Introduction <./resources/django-rest-framework/01-introduction.rst>`_ - REST principles and setup
* `📝 Serializers <./resources/django-rest-framework/02-serializers.rst>`_ - Data validation and transformation
* `🏗️ Views & ViewSets <./resources/django-rest-framework/03-views-viewsets.rst>`_ - API endpoint creation
* `🔐 Authentication <./resources/django-rest-framework/04-authentication.rst>`_ - Securing your API
* `🛡️ Permissions <./resources/django-rest-framework/05-permissions.rst>`_ - Access control

🏗️ **Project Documentation**
----------------------------

Understand this specific application:

* `🏛️ Architecture Guide <./resources/project-documentation/architecture.rst>`_ - System design and data flow

🛠️ Development Setup
====================

Prerequisites
-------------

* **Python 3.12+** - Backend runtime
* **Node.js 20+** - Frontend build tools
* **Git** - Version control

Backend Setup
-------------

.. code-block:: bash

    # 1. Clone the repository
    git clone <repository-url>
    cd django_application

    # 2. Set up Python virtual environment
    cd backend
    python -m venv venv
    
    # Activate virtual environment
    # On macOS/Linux:
    source venv/bin/activate

    # 3. Install Python dependencies
    pip install -r requirements.txt

    # 4. Set up database
    python manage.py migrate

    # 5. Create admin user (optional)
    python manage.py createsuperuser

    # 6. Run development server
    python manage.py runserver

**Backend will be available at:** http://localhost:8000

Frontend Setup
--------------

.. code-block:: bash

    # 1. Navigate to frontend directory
    cd frontend

    # 2. Install Node.js dependencies
    npm install

    # 3. Start development server
    npm start

**Frontend will be available at:** http://localhost:3000

🧪 Testing
==========

Backend Tests
-------------

.. code-block:: bash

    cd backend
    
    # Run all tests
    python manage.py test
    
    # Run specific test modules
    python manage.py test tests.test_models
    python manage.py test tests.test_task_api
    python manage.py test tests.test_todo_api
    

Code Quality
------------

.. code-block:: bash

    # Run pylint for code quality checks
    python -m pylint app/
    python -m pylint tests/
    
    # Check specific files
    python -m pylint app/models/task_model.py

Test Coverage
-------------

Our test suite covers:

* ✅ **Model Tests**: Data validation and relationships
* ✅ **API Tests**: All CRUD operations and edge cases
* ✅ **Authentication Tests**: Login, logout, and token validation
* ✅ **Permission Tests**: User data isolation
* ✅ **Integration Tests**: Complete user workflows

📊 API Reference
================

The application provides a complete RESTful API. Here are the main endpoints:

Authentication
--------------

.. code-block:: text

    POST   /api/auth/login/     # Login (returns token)
    POST   /logout/             # Logout

Tasks
-----

.. code-block:: text

    GET    /api/tasks/          # List user's tasks
    POST   /api/tasks/          # Create new task
    GET    /api/tasks/{id}/     # Get specific task
    PUT    /api/tasks/{id}/     # Update task
    PATCH  /api/tasks/{id}/     # Partial update
    DELETE /api/tasks/{id}/     # Delete task

Todos
-----

.. code-block:: text

    GET    /api/todos/          # List user's todos
    POST   /api/todos/          # Create new todo
    GET    /api/todos/{id}/     # Get specific todo
    PUT    /api/todos/{id}/     # Update todo
    PATCH  /api/todos/{id}/     # Partial update
    DELETE /api/todos/{id}/     # Delete todo
    POST   /api/todos/{id}/toggle_complete/  # Toggle completion

**Authentication:** All API endpoints require a valid token in the Authorization header:

.. code-block:: text

    Authorization: Token <your-token-here>

🚀 Deployment
=============

Production Checklist
--------------------

Backend (Django)
~~~~~~~~~~~~~~~~

.. code-block:: python

    # settings.py for production
    DEBUG = False
    ALLOWED_HOSTS = ['your-domain.com']
    
    # Use environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Database (PostgreSQL recommended)
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

Frontend (React)
~~~~~~~~~~~~~~~

.. code-block:: bash

    # Build for production
    npm run build
    
    # Serve static files (example with serve)
    npm install -g serve
    serve -s build

Development Guidelines
---------------------

* ✅ Write tests for new features
* ✅ Follow PEP 8 style guidelines
* ✅ Update documentation for API changes
* ✅ Ensure all tests pass
* ✅ Maintain code quality standards

🆘 Support
==========

Need Help?
----------

* 📚 **Documentation**: Start with our comprehensive guides in ``./resources/``
* 🐛 **Issues**: Report bugs or request features via GitHub Issues
* 💡 **Questions**: Check our learning resources or open a discussion

Learning Path
-------------

1. **Complete Beginner**: Start with `Django Basics <./resources/django-basics/>`_
2. **API Development**: Move to `DRF Guides <./resources/django-rest-framework/>`_
3. **This Application**: Study `Project Documentation <./resources/project-documentation/>`_
4. **Advanced Topics**: Explore deployment and scaling

🏆 Features Showcase
===================

**Task Management**

* Create and organize tasks with descriptions
* Mark tasks as complete/incomplete
* Associate todos with specific tasks

**Todo System**

* Add todos to tasks or create standalone todos
* Set due dates and add custom tags
* Toggle completion status with real-time updates

**User Experience**

* Responsive design works on all devices
* Dark theme with modern Material-UI components
* Instant feedback for all user actions

**Security**

* Token-based authentication
* User data isolation
* Protected API endpoints

**Developer Experience**

* Well-documented codebase
* Comprehensive test coverage
* Code quality enforcement
* Clear project structure

---

**Ready to build amazing task management applications?** Start with our `learning resources <./resources/>`_ and explore the codebase! 🚀

**Questions?** Check out our comprehensive documentation or open an issue for support.