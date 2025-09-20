===========================
DRF Permissions Guide
===========================

Permissions in Django REST Framework determine whether a request should be granted or denied access. They work hand-in-hand with authentication to control what users can do with your API.

🎯 Understanding Permissions
============================

Permissions answer the question: **"Is this user allowed to perform this action?"**

**Key Concepts:**

* **Authentication**: Who is the user? (handled by authentication classes)
* **Permissions**: What can this user do? (handled by permission classes)
* **Authorization**: The combination of authentication + permissions

Permission Flow
---------------

.. code-block:: text

    Request → Authentication → Permissions → View → Response
                    ↓               ↓
              Identifies user   Checks access
              (or anonymous)    permissions

🛡️ Built-in Permission Classes
==============================

DRF provides several built-in permission classes:

AllowAny
--------

Allows unrestricted access, regardless of authentication:

.. code-block:: python

    from rest_framework.permissions import AllowAny
    from rest_framework import viewsets

    class PublicTaskViewSet(viewsets.ReadOnlyModelViewSet):
        """Public read-only access to tasks."""
        permission_classes = [AllowAny]
        serializer_class = TaskSerializer
        queryset = Task.objects.filter(is_public=True)

IsAuthenticated
---------------

Denies permission to any unauthenticated user:

.. code-block:: python

    from rest_framework.permissions import IsAuthenticated

    class TaskViewSet(viewsets.ModelViewSet):
        """Only authenticated users can access tasks."""
        permission_classes = [IsAuthenticated]
        serializer_class = TaskSerializer
        
        def get_queryset(self):
            return Task.objects.filter(user=self.request.user)

IsAuthenticatedOrReadOnly
-------------------------

Allows read access to everyone, write access only to authenticated users:

.. code-block:: python

    from rest_framework.permissions import IsAuthenticatedOrReadOnly

    class TaskViewSet(viewsets.ModelViewSet):
        """Anyone can read, only authenticated users can write."""
        permission_classes = [IsAuthenticatedOrReadOnly]
        serializer_class = TaskSerializer
        queryset = Task.objects.all()

IsAdminUser
-----------

Only allows access to users with ``is_staff=True``:

.. code-block:: python

    from rest_framework.permissions import IsAdminUser

    class AdminTaskViewSet(viewsets.ModelViewSet):
        """Only admin users can access this view."""
        permission_classes = [IsAdminUser]
        serializer_class = TaskSerializer
        queryset = Task.objects.all()

🏗️ Custom Permission Classes
============================

Create custom permissions by inheriting from ``BasePermission``:

Basic Custom Permission
-----------------------

.. code-block:: python

    from rest_framework import permissions

    class IsOwnerOrReadOnly(permissions.BasePermission):
        """
        Custom permission to only allow owners of an object to edit it.
        """

        def has_object_permission(self, request, view, obj):
            # Read permissions for any request (GET, HEAD, OPTIONS)
            if request.method in permissions.SAFE_METHODS:
                return True

            # Write permissions only to the owner of the object
            return obj.user == request.user

    class TaskViewSet(viewsets.ModelViewSet):
        permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        serializer_class = TaskSerializer
        
        def get_queryset(self):
            return Task.objects.filter(user=self.request.user)

Advanced Custom Permissions
---------------------------

.. code-block:: python

    class IsOwnerOrAdmin(permissions.BasePermission):
        """
        Permission that allows:
        - Owners to have full access to their objects
        - Admins to have full access to all objects
        - Others to have read-only access
        """
        
        def has_permission(self, request, view):
            """Check view-level permissions."""
            # Allow authenticated users to list/create
            return request.user and request.user.is_authenticated
        
        def has_object_permission(self, request, view, obj):
            """Check object-level permissions."""
            # Admins can do anything
            if request.user.is_staff:
                return True
            
            # Read permissions for any authenticated user
            if request.method in permissions.SAFE_METHODS:
                return True
            
            # Write permissions only for owners
            return obj.user == request.user

    class TaskPriorityPermission(permissions.BasePermission):
        """Only allow high-priority tasks to be edited by managers."""
        
        def has_object_permission(self, request, view, obj):
            # Anyone can read
            if request.method in permissions.SAFE_METHODS:
                return True
            
            # High priority tasks require manager role
            if hasattr(obj, 'priority') and obj.priority == 'high':
                return hasattr(request.user, 'profile') and request.user.profile.is_manager
            
            # Regular tasks can be edited by owners
            return obj.user == request.user

🎯 Our Todo App Permissions
===========================

Task Permissions
----------------

.. code-block:: python

    from rest_framework import permissions

    class IsTaskOwner(permissions.BasePermission):
        """
        Permission class for Task model.
        - Owners can perform all operations on their tasks
        - Others cannot access tasks they don't own
        """
        
        def has_permission(self, request, view):
            """Allow authenticated users to access the view."""
            return request.user and request.user.is_authenticated
        
        def has_object_permission(self, request, view, obj):
            """Check if user can access this specific task."""
            return obj.user == request.user

    class TaskViewSet(viewsets.ModelViewSet):
        serializer_class = TaskSerializer
        permission_classes = [IsAuthenticated, IsTaskOwner]
        
        def get_queryset(self):
            # Users only see their own tasks
            return Task.objects.filter(user=self.request.user)
        
        def perform_create(self, serializer):
            # Automatically assign task to current user
            serializer.save(user=self.request.user)

Todo Permissions
----------------

.. code-block:: python

    class IsTodoOwnerOrTaskOwner(permissions.BasePermission):
        """
        Permission for Todo model.
        - Todo owner can edit their todos
        - Task owner can edit todos in their tasks
        - Others cannot access
        """
        
        def has_permission(self, request, view):
            return request.user and request.user.is_authenticated
        
        def has_object_permission(self, request, view, obj):
            # Todo owner has full access
            if obj.user == request.user:
                return True
            
            # Task owner can also edit todos in their tasks
            if obj.task and obj.task.user == request.user:
                return True
            
            return False

    class TodoViewSet(viewsets.ModelViewSet):
        serializer_class = TodoSerializer
        permission_classes = [IsAuthenticated, IsTodoOwnerOrTaskOwner]
        
        def get_queryset(self):
            # Users see todos they own or todos in their tasks
            return Todo.objects.filter(
                Q(user=self.request.user) | 
                Q(task__user=self.request.user)
            )

🔧 Permission Combinations
==========================

Multiple Permissions
--------------------

Combine multiple permission classes (ALL must pass):

.. code-block:: python

    class TaskViewSet(viewsets.ModelViewSet):
        permission_classes = [
            IsAuthenticated,     # Must be logged in
            IsOwnerOrReadOnly,   # Must own object to edit
            IsNotBlocked         # Must not be blocked user
        ]

Custom Permission Logic
-----------------------

.. code-block:: python

    class CustomTaskPermission(permissions.BasePermission):
        """Complex permission logic for tasks."""
        
        def has_permission(self, request, view):
            """View-level permission check."""
            if not request.user.is_authenticated:
                return False
            
            # Block suspended users
            if hasattr(request.user, 'profile') and request.user.profile.is_suspended:
                return False
            
            # Limit creation for free users
            if view.action == 'create':
                user_task_count = Task.objects.filter(user=request.user).count()
                if not request.user.profile.is_premium and user_task_count >= 10:
                    return False
            
            return True
        
        def has_object_permission(self, request, view, obj):
            """Object-level permission check."""
            # Owners can do anything
            if obj.user == request.user:
                return True
            
            # Team members can view shared tasks
            if view.action in ['retrieve', 'list']:
                return obj.team_members.filter(id=request.user.id).exists()
            
            return False

🎨 Dynamic Permissions
======================

Per-Action Permissions
---------------------

.. code-block:: python

    class TaskViewSet(viewsets.ModelViewSet):
        serializer_class = TaskSerializer
        
        def get_permissions(self):
            """
            Instantiate and return the list of permissions for this view.
            """
            if self.action == 'list':
                permission_classes = [IsAuthenticated]
            elif self.action == 'create':
                permission_classes = [IsAuthenticated]
            elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
                permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
            elif self.action == 'toggle_complete':
                permission_classes = [IsAuthenticated, IsTaskOwner]
            else:
                permission_classes = [IsAuthenticated]
            
            return [permission() for permission in permission_classes]

User Role-Based Permissions
---------------------------

.. code-block:: python

    class RoleBasedPermission(permissions.BasePermission):
        """Permission based on user roles."""
        
        # Define what each role can do
        ROLE_PERMISSIONS = {
            'admin': ['create', 'read', 'update', 'delete'],
            'manager': ['create', 'read', 'update'],
            'member': ['read', 'update_own'],
            'viewer': ['read'],
        }
        
        def has_permission(self, request, view):
            if not request.user.is_authenticated:
                return False
            
            user_role = getattr(request.user, 'role', 'viewer')
            allowed_actions = self.ROLE_PERMISSIONS.get(user_role, [])
            
            # Map view actions to permission actions
            action_map = {
                'list': 'read',
                'retrieve': 'read',
                'create': 'create',
                'update': 'update',
                'partial_update': 'update',
                'destroy': 'delete',
            }
            
            required_action = action_map.get(view.action, 'read')
            return required_action in allowed_actions
        
        def has_object_permission(self, request, view, obj):
            user_role = getattr(request.user, 'role', 'viewer')
            
            # Admin can do anything
            if user_role == 'admin':
                return True
            
            # Members can only update their own objects
            if user_role == 'member' and view.action in ['update', 'partial_update']:
                return obj.user == request.user
            
            # Default object permission logic
            return obj.user == request.user

🔐 Permission with User Groups
==============================

Django Groups Integration
-------------------------

.. code-block:: python

    from django.contrib.auth.models import Group

    class GroupBasedPermission(permissions.BasePermission):
        """Permission based on Django groups."""
        
        def has_permission(self, request, view):
            if not request.user.is_authenticated:
                return False
            
            # Check if user belongs to required groups
            required_groups = getattr(view, 'required_groups', [])
            if required_groups:
                user_groups = request.user.groups.values_list('name', flat=True)
                return any(group in user_groups for group in required_groups)
            
            return True

    class TaskViewSet(viewsets.ModelViewSet):
        serializer_class = TaskSerializer
        permission_classes = [IsAuthenticated, GroupBasedPermission]
        required_groups = ['task_managers', 'administrators']

Custom Group Permissions
------------------------

.. code-block:: python

    class TeamPermission(permissions.BasePermission):
        """Permission based on team membership."""
        
        def has_permission(self, request, view):
            if not request.user.is_authenticated:
                return False
            
            # Allow if user belongs to any team
            return hasattr(request.user, 'teams') and request.user.teams.exists()
        
        def has_object_permission(self, request, view, obj):
            # Check if user's team has access to this object
            if hasattr(obj, 'team'):
                return request.user.teams.filter(id=obj.team.id).exists()
            
            # Default to owner check
            return obj.user == request.user

    class ProjectPermission(permissions.BasePermission):
        """Permission based on project access."""
        
        def has_object_permission(self, request, view, obj):
            # Get the project from the object
            project = getattr(obj, 'project', None)
            if not project:
                return obj.user == request.user
            
            # Check project access levels
            project_access = project.get_user_access_level(request.user)
            
            action_requirements = {
                'read': ['viewer', 'contributor', 'maintainer', 'owner'],
                'create': ['contributor', 'maintainer', 'owner'],
                'update': ['maintainer', 'owner'],
                'delete': ['owner'],
            }
            
            view_action = getattr(view, 'action', 'read')
            required_levels = action_requirements.get(view_action, ['owner'])
            
            return project_access in required_levels

🧪 Testing Permissions
======================

Permission Testing
------------------

.. code-block:: python

    from rest_framework.test import APITestCase
    from rest_framework import status
    from django.contrib.auth.models import User
    from rest_framework.authtoken.models import Token
    from .models import Task, Todo

    class PermissionTest(APITestCase):
        def setUp(self):
            """Set up test users and data."""
            self.user1 = User.objects.create_user('user1', 'user1@test.com', 'pass')
            self.user2 = User.objects.create_user('user2', 'user2@test.com', 'pass')
            
            self.token1 = Token.objects.create(user=self.user1)
            self.token2 = Token.objects.create(user=self.user2)
            
            self.task1 = Task.objects.create(
                title='User1 Task',
                description='Task owned by user1',
                user=self.user1
            )
            
            self.task2 = Task.objects.create(
                title='User2 Task', 
                description='Task owned by user2',
                user=self.user2
            )
        
        def test_user_can_access_own_tasks(self):
            """Test user can access their own tasks."""
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
            
            response = self.client.get('/api/tasks/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            # Should only see own tasks
            task_ids = [task['id'] for task in response.data]
            self.assertIn(self.task1.id, task_ids)
            self.assertNotIn(self.task2.id, task_ids)
        
        def test_user_cannot_access_others_tasks(self):
            """Test user cannot access another user's task."""
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
            
            response = self.client.get(f'/api/tasks/{self.task2.id}/')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        def test_user_can_edit_own_task(self):
            """Test user can edit their own task."""
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
            
            data = {'title': 'Updated Task Title'}
            response = self.client.patch(f'/api/tasks/{self.task1.id}/', data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            self.task1.refresh_from_db()
            self.assertEqual(self.task1.title, 'Updated Task Title')
        
        def test_user_cannot_edit_others_task(self):
            """Test user cannot edit another user's task."""
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
            
            data = {'title': 'Malicious Update'}
            response = self.client.patch(f'/api/tasks/{self.task2.id}/', data)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        def test_unauthenticated_access_denied(self):
            """Test unauthenticated users cannot access tasks."""
            response = self.client.get('/api/tasks/')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        def test_invalid_token_access_denied(self):
            """Test invalid token is rejected."""
            self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token')
            response = self.client.get('/api/tasks/')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

Custom Permission Testing
-------------------------

.. code-block:: python

    class CustomPermissionTest(APITestCase):
        def setUp(self):
            self.admin_user = User.objects.create_user(
                'admin', 'admin@test.com', 'pass'
            )
            self.admin_user.is_staff = True
            self.admin_user.save()
            
            self.regular_user = User.objects.create_user(
                'user', 'user@test.com', 'pass'
            )
            
            self.admin_token = Token.objects.create(user=self.admin_user)
            self.user_token = Token.objects.create(user=self.regular_user)
        
        def test_admin_can_access_all_tasks(self):
            """Test admin users can access all tasks."""
            # Create tasks for different users
            Task.objects.create(title='Task 1', user=self.regular_user)
            Task.objects.create(title='Task 2', user=self.admin_user)
            
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
            response = self.client.get('/api/admin/tasks/')
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 2)  # Should see all tasks
        
        def test_regular_user_cannot_access_admin_endpoints(self):
            """Test regular users cannot access admin endpoints."""
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
            response = self.client.get('/api/admin/tasks/')
            
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

🎨 Advanced Permission Patterns
===============================

Conditional Permissions
-----------------------

.. code-block:: python

    class ConditionalPermission(permissions.BasePermission):
        """Permission based on object state and user attributes."""
        
        def has_object_permission(self, request, view, obj):
            # Allow read access to published tasks
            if request.method in permissions.SAFE_METHODS:
                return obj.is_published or obj.user == request.user
            
            # Write access rules
            if obj.user == request.user:
                # Owners can edit if not locked
                return not getattr(obj, 'is_locked', False)
            
            # Collaborators can edit if explicitly allowed
            if hasattr(obj, 'collaborators'):
                collaboration = obj.collaborators.filter(user=request.user).first()
                if collaboration:
                    return collaboration.can_edit
            
            return False

Time-Based Permissions
---------------------

.. code-block:: python

    from django.utils import timezone
    from datetime import timedelta

    class TimeBasedPermission(permissions.BasePermission):
        """Permission that changes based on time."""
        
        def has_object_permission(self, request, view, obj):
            # Basic owner check
            if obj.user != request.user:
                return False
            
            # Check if object is in edit window
            if hasattr(obj, 'created_at'):
                edit_deadline = obj.created_at + timedelta(hours=24)
                if timezone.now() > edit_deadline:
                    # Can only read after edit deadline
                    return request.method in permissions.SAFE_METHODS
            
            return True

Rate-Limited Permissions
-----------------------

.. code-block:: python

    from django.core.cache import cache

    class RateLimitedPermission(permissions.BasePermission):
        """Permission with rate limiting."""
        
        def has_permission(self, request, view):
            if view.action != 'create':
                return True
            
            # Check rate limit for task creation
            user_id = request.user.id
            cache_key = f'task_creation_rate_{user_id}'
            
            # Get current count
            current_count = cache.get(cache_key, 0)
            
            # Limit: 10 tasks per hour
            if current_count >= 10:
                return False
            
            # Increment counter
            cache.set(cache_key, current_count + 1, 3600)  # 1 hour TTL
            return True

🔒 Security Best Practices
==========================

1. **Defense in Depth**
   - Use multiple layers of permissions
   - Don't rely on frontend validation alone

2. **Principle of Least Privilege**
   - Grant minimum necessary permissions
   - Default to restrictive permissions

3. **Object-Level Security**
   - Always filter querysets by user
   - Check object ownership in permissions

4. **Audit and Logging**
   - Log permission denials
   - Monitor suspicious access patterns

5. **Regular Review**
   - Periodically review permission logic
   - Test edge cases and attack scenarios

Example Security Implementation
------------------------------

.. code-block:: python

    import logging
    from django.core.exceptions import PermissionDenied

    logger = logging.getLogger('security')

    class SecureTaskPermission(permissions.BasePermission):
        """Security-focused permission class."""
        
        def has_permission(self, request, view):
            # Log all access attempts
            logger.info(
                f"Permission check: {request.user} accessing {view.__class__.__name__} "
                f"with action {getattr(view, 'action', 'unknown')}"
            )
            
            if not request.user.is_authenticated:
                logger.warning(f"Unauthenticated access attempt from {request.META.get('REMOTE_ADDR')}")
                return False
            
            # Check for suspended users
            if hasattr(request.user, 'profile') and request.user.profile.is_suspended:
                logger.warning(f"Suspended user {request.user} attempted access")
                return False
            
            return True
        
        def has_object_permission(self, request, view, obj):
            # Check ownership
            if obj.user != request.user:
                logger.warning(
                    f"User {request.user} attempted to access object {obj.id} "
                    f"owned by {obj.user}"
                )
                return False
            
            # Check for locked objects
            if getattr(obj, 'is_locked', False) and request.method not in permissions.SAFE_METHODS:
                logger.warning(
                    f"User {request.user} attempted to modify locked object {obj.id}"
                )
                return False
            
            return True

📖 Error Handling
=================

Custom Permission Errors
------------------------

.. code-block:: python

    from rest_framework.exceptions import PermissionDenied

    class CustomTaskPermission(permissions.BasePermission):
        """Permission with custom error messages."""
        
        def has_permission(self, request, view):
            if not request.user.is_authenticated:
                raise PermissionDenied("Authentication required to access tasks.")
            
            if view.action == 'create':
                user_task_count = Task.objects.filter(user=request.user).count()
                if user_task_count >= 100:
                    raise PermissionDenied(
                        "You have reached the maximum number of tasks (100). "
                        "Please delete some tasks before creating new ones."
                    )
            
            return True
        
        def has_object_permission(self, request, view, obj):
            if obj.user != request.user:
                raise PermissionDenied(
                    "You can only access your own tasks. "
                    f"This task belongs to {obj.user.username}."
                )
            
            return True

🎓 Best Practices Summary
=========================

1. **Use Built-in Permissions First**
   - Start with DRF's built-in permissions
   - Create custom permissions only when needed

2. **Keep Permissions Simple**
   - Each permission class should have a single responsibility
   - Complex logic should be broken into multiple permissions

3. **Test Thoroughly**
   - Test all permission scenarios
   - Include edge cases and attack vectors

4. **Document Permission Logic**
   - Clear docstrings explaining permission rules
   - Document any complex business logic

5. **Monitor and Log**
   - Log permission failures for security monitoring
   - Track unusual access patterns


🔗 Resources
============

* 📚 `DRF Permissions Documentation <https://www.django-rest-framework.org/api-guide/permissions/>`_
* 🔐 `Django Permissions <https://docs.djangoproject.com/en/stable/topics/auth/default/#permissions-and-authorization>`_
* 🛡️ `Security Best Practices <https://docs.djangoproject.com/en/stable/topics/security/>`_

---

Permissions are crucial for API security! With proper permission classes, you can ensure users only access what they're supposed to, keeping your data safe and secure. 🔒

Ready to add advanced filtering? Let's explore `Filtering and Searching <./06-filtering.rst>`_ next!