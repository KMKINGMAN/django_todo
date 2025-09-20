============================
Authentication in DRF Guide
============================

Authentication in Django REST Framework determines who is making the request. DRF provides multiple authentication schemes to secure your API endpoints.

🎯 Understanding Authentication
==============================

Authentication answers the question: **"Who is this user?"**

* **Authentication**: Identifying the user making the request
* **Authorization**: Determining what the authenticated user can do (handled by permissions)

DRF supports multiple authentication methods that can be used together:

.. code-block:: python

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework.authentication.BasicAuthentication',
        ],
    }

🔑 Authentication Types
======================

1. **Session Authentication** - Uses Django's session framework
2. **Token Authentication** - Simple token-based authentication
3. **Basic Authentication** - HTTP Basic authentication
4. **JWT Authentication** - JSON Web Token authentication (third-party)

🎫 Token Authentication (Recommended)
=====================================

Token authentication is stateless and perfect for API-only applications:

Setup
-----

.. code-block:: python

    # settings.py
    INSTALLED_APPS = [
        # ... other apps
        'rest_framework',
        'rest_framework.authtoken',  # Add this
    ]

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.TokenAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
    }

.. code-block:: bash

    # Run migrations to create token table
    python manage.py migrate

Creating Tokens
---------------

.. code-block:: python

    # Method 1: Create tokens for existing users
    python manage.py drf_create_token <username>

    # Method 2: Programmatically
    from rest_framework.authtoken.models import Token
    from django.contrib.auth.models import User

    user = User.objects.get(username='john')
    token = Token.objects.create(user=user)
    print(token.key)

    # Method 3: Auto-create tokens for new users
    from django.db.models.signals import post_save
    from django.dispatch import receiver
    from django.contrib.auth.models import User
    from rest_framework.authtoken.models import Token

    @receiver(post_save, sender=User)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)

🏗️ Custom Login API
===================

Our Todo App Login Implementation
---------------------------------

.. code-block:: python

    # views/auth_views.py
    from rest_framework.views import APIView
    from rest_framework.response import Response
    from rest_framework import status
    from django.contrib.auth import authenticate
    from rest_framework.authtoken.models import Token

    class APILoginView(APIView):
        """Custom login view that returns authentication token."""
        
        def post(self, request):
            """
            Authenticate user and return token.
            
            POST /api/auth/login/
            {
                "username": "john",
                "password": "password123"
            }
            
            Response:
            {
                "token": "abc123...",
                "user_id": 1,
                "username": "john"
            }
            """
            username = request.data.get('username')
            password = request.data.get('password')
            
            if not username or not password:
                return Response(
                    {'error': 'Username and password are required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Authenticate user
            user = authenticate(username=username, password=password)
            
            if user:
                # Get or create token
                token, created = Token.objects.get_or_create(user=user)
                
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                })
            else:
                return Response(
                    {'error': 'Invalid credentials'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

    class APILogoutView(APIView):
        """Logout view that deletes the user's token."""
        
        def post(self, request):
            """
            Logout user by deleting their token.
            
            POST /api/auth/logout/
            Headers: Authorization: Token abc123...
            """
            try:
                # Delete the user's token
                request.user.auth_token.delete()
                return Response({'message': 'Successfully logged out'})
            except:
                return Response(
                    {'error': 'Error logging out'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

URL Configuration
-----------------

.. code-block:: python

    # urls.py
    from django.urls import path, include
    from app.views.auth_views import APILoginView, APILogoutView

    urlpatterns = [
        path('api/auth/login/', APILoginView.as_view(), name='api-login'),
        path('api/auth/logout/', APILogoutView.as_view(), name='api-logout'),
        path('api/', include(router.urls)),
    ]

🖥️ Frontend Integration
=======================

JavaScript/React Implementation
-------------------------------

.. code-block:: javascript

    // API service for authentication
    class AuthService {
        constructor() {
            this.baseURL = 'http://localhost:8000/api';
        }
        
        async login(username, password) {
            try {
                const response = await fetch(`${this.baseURL}/auth/login/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password }),
                });
                
                if (response.ok) {
                    const data = await response.json();
                    // Store token in localStorage
                    localStorage.setItem('auth_token', data.token);
                    localStorage.setItem('user_id', data.user_id);
                    localStorage.setItem('username', data.username);
                    return data;
                } else {
                    const error = await response.json();
                    throw new Error(error.error || 'Login failed');
                }
            } catch (error) {
                console.error('Login error:', error);
                throw error;
            }
        }
        
        async logout() {
            const token = localStorage.getItem('auth_token');
            
            if (token) {
                try {
                    await fetch(`${this.baseURL}/auth/logout/`, {
                        method: 'POST',
                        headers: {
                            'Authorization': `Token ${token}`,
                            'Content-Type': 'application/json',
                        },
                    });
                } catch (error) {
                    console.error('Logout error:', error);
                }
            }
            
            // Clear stored data
            localStorage.removeItem('auth_token');
            localStorage.removeItem('user_id');
            localStorage.removeItem('username');
        }
        
        getToken() {
            return localStorage.getItem('auth_token');
        }
        
        isAuthenticated() {
            return !!this.getToken();
        }
        
        getUser() {
            return {
                id: localStorage.getItem('user_id'),
                username: localStorage.getItem('username'),
            };
        }
    }

    // Usage in components
    const authService = new AuthService();

    // Login component
    const handleLogin = async (username, password) => {
        try {
            const userData = await authService.login(username, password);
            console.log('Login successful:', userData);
            // Redirect to dashboard
            window.location.href = '/dashboard';
        } catch (error) {
            console.error('Login failed:', error.message);
            // Show error message to user
        }
    };

    // API requests with authentication
    const fetchTasks = async () => {
        const token = authService.getToken();
        
        try {
            const response = await fetch('http://localhost:8000/api/tasks/', {
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json',
                },
            });
            
            if (response.ok) {
                const tasks = await response.json();
                return tasks;
            } else {
                throw new Error('Failed to fetch tasks');
            }
        } catch (error) {
            console.error('Error fetching tasks:', error);
            throw error;
        }
    };

React Context for Authentication
-------------------------------

.. code-block:: javascript

    // AuthContext.js
    import React, { createContext, useContext, useState, useEffect } from 'react';

    const AuthContext = createContext();

    export const useAuth = () => {
        const context = useContext(AuthContext);
        if (!context) {
            throw new Error('useAuth must be used within an AuthProvider');
        }
        return context;
    };

    export const AuthProvider = ({ children }) => {
        const [user, setUser] = useState(null);
        const [loading, setLoading] = useState(true);
        
        useEffect(() => {
            // Check if user is logged in on app start
            const token = localStorage.getItem('auth_token');
            if (token) {
                setUser({
                    id: localStorage.getItem('user_id'),
                    username: localStorage.getItem('username'),
                    token: token,
                });
            }
            setLoading(false);
        }, []);
        
        const login = async (username, password) => {
            try {
                const response = await fetch('/api/auth/login/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password }),
                });
                
                if (response.ok) {
                    const userData = await response.json();
                    
                    // Store in localStorage
                    localStorage.setItem('auth_token', userData.token);
                    localStorage.setItem('user_id', userData.user_id);
                    localStorage.setItem('username', userData.username);
                    
                    // Update state
                    setUser(userData);
                    
                    return userData;
                } else {
                    const error = await response.json();
                    throw new Error(error.error);
                }
            } catch (error) {
                throw error;
            }
        };
        
        const logout = async () => {
            const token = localStorage.getItem('auth_token');
            
            if (token) {
                try {
                    await fetch('/api/auth/logout/', {
                        method: 'POST',
                        headers: { 'Authorization': `Token ${token}` },
                    });
                } catch (error) {
                    console.error('Logout error:', error);
                }
            }
            
            // Clear storage and state
            localStorage.removeItem('auth_token');
            localStorage.removeItem('user_id');
            localStorage.removeItem('username');
            setUser(null);
        };
        
        const value = {
            user,
            login,
            logout,
            loading,
            isAuthenticated: !!user,
        };
        
        return (
            <AuthContext.Provider value={value}>
                {children}
            </AuthContext.Provider>
        );
    };

🛡️ Protected Routes
===================

Route Protection in Views
-------------------------

.. code-block:: python

    from rest_framework.permissions import IsAuthenticated
    from rest_framework import viewsets

    class TaskViewSet(viewsets.ModelViewSet):
        """Tasks are only accessible to authenticated users."""
        permission_classes = [IsAuthenticated]
        
        def get_queryset(self):
            # Only return tasks for the authenticated user
            return Task.objects.filter(user=self.request.user)

Frontend Route Protection
------------------------

.. code-block:: javascript

    // ProtectedRoute.js
    import React from 'react';
    import { Navigate } from 'react-router-dom';
    import { useAuth } from './AuthContext';

    const ProtectedRoute = ({ children }) => {
        const { isAuthenticated, loading } = useAuth();
        
        if (loading) {
            return <div>Loading...</div>;
        }
        
        return isAuthenticated ? children : <Navigate to="/login" />;
    };

    // App.js
    import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
    import { AuthProvider } from './AuthContext';

    function App() {
        return (
            <AuthProvider>
                <Router>
                    <Routes>
                        <Route path="/login" element={<LoginPage />} />
                        <Route 
                            path="/dashboard" 
                            element={
                                <ProtectedRoute>
                                    <DashboardPage />
                                </ProtectedRoute>
                            } 
                        />
                        <Route 
                            path="/tasks" 
                            element={
                                <ProtectedRoute>
                                    <TaskListPage />
                                </ProtectedRoute>
                            } 
                        />
                    </Routes>
                </Router>
            </AuthProvider>
        );
    }

🔧 Advanced Authentication
==========================

Custom Token Model
------------------

.. code-block:: python

    # models.py
    from django.contrib.auth.models import User
    from django.db import models
    import binascii
    import os

    class APIToken(models.Model):
        """Custom token model with expiration."""
        key = models.CharField(max_length=40, primary_key=True)
        user = models.OneToOneField(User, related_name='api_token', on_delete=models.CASCADE)
        created = models.DateTimeField(auto_now_add=True)
        expires_at = models.DateTimeField()
        
        def save(self, *args, **kwargs):
            if not self.key:
                self.key = self.generate_key()
            return super().save(*args, **kwargs)
        
        def generate_key(self):
            return binascii.hexlify(os.urandom(20)).decode()
        
        def is_expired(self):
            from django.utils import timezone
            return timezone.now() > self.expires_at

Custom Authentication Class
---------------------------

.. code-block:: python

    # authentication.py
    from rest_framework.authentication import TokenAuthentication
    from rest_framework.exceptions import AuthenticationFailed
    from django.utils import timezone

    class ExpiringTokenAuthentication(TokenAuthentication):
        """Token authentication with expiration."""
        
        def authenticate_credentials(self, key):
            model = self.get_model()
            try:
                token = model.objects.select_related('user').get(key=key)
            except model.DoesNotExist:
                raise AuthenticationFailed('Invalid token.')
            
            if not token.user.is_active:
                raise AuthenticationFailed('User inactive or deleted.')
            
            # Check if token is expired
            if hasattr(token, 'is_expired') and token.is_expired():
                raise AuthenticationFailed('Token has expired.')
            
            return (token.user, token)

Multiple Authentication Methods
------------------------------

.. code-block:: python

    # settings.py
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',  # For web interface
            'rest_framework.authentication.TokenAuthentication',    # For API clients
        ],
    }

    # This allows both session and token authentication
    # Useful when you have both web interface and API clients

🔒 Session Authentication
========================

Session authentication uses Django's built-in session framework:

.. code-block:: python

    # settings.py
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',
        ],
    }

    # Also include CSRF protection
    from django.middleware.csrf import get_token

    class CSRFTokenView(APIView):
        """Get CSRF token for session authentication."""
        permission_classes = [AllowAny]
        
        def get(self, request):
            return Response({'csrf_token': get_token(request)})

Frontend Session Authentication
------------------------------

.. code-block:: javascript

    // For session authentication, include CSRF token
    const getCsrfToken = async () => {
        const response = await fetch('/api/csrf-token/');
        const data = await response.json();
        return data.csrf_token;
    };

    const loginWithSession = async (username, password) => {
        const csrfToken = await getCsrfToken();
        
        const response = await fetch('/api/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            credentials: 'include',  // Include cookies
            body: JSON.stringify({ username, password }),
        });
        
        return response.json();
    };

🧪 Testing Authentication
=========================

.. code-block:: python

    from rest_framework.test import APITestCase
    from rest_framework import status
    from django.contrib.auth.models import User
    from rest_framework.authtoken.models import Token

    class AuthenticationTest(APITestCase):
        def setUp(self):
            self.user = User.objects.create_user(
                username='testuser',
                password='testpass123'
            )
            self.token = Token.objects.create(user=self.user)
        
        def test_token_authentication(self):
            """Test that token authentication works."""
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
            response = self.client.get('/api/tasks/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        def test_unauthenticated_request(self):
            """Test that unauthenticated requests are rejected."""
            response = self.client.get('/api/tasks/')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        def test_invalid_token(self):
            """Test that invalid tokens are rejected."""
            self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token')
            response = self.client.get('/api/tasks/')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        def test_login_api(self):
            """Test the login API endpoint."""
            data = {
                'username': 'testuser',
                'password': 'testpass123'
            }
            response = self.client.post('/api/auth/login/', data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('token', response.data)
        
        def test_logout_api(self):
            """Test the logout API endpoint."""
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
            response = self.client.post('/api/auth/logout/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            # Token should be deleted
            self.assertFalse(Token.objects.filter(key=self.token.key).exists())

🎓 Best Practices
=================

1. **Use HTTPS in Production**
   - Always use HTTPS to protect tokens in transit
   - Never send authentication data over HTTP

2. **Store Tokens Securely**
   - Use secure storage on mobile apps
   - Consider token expiration
   - Implement token refresh if needed

3. **Handle Token Expiration**
   - Implement automatic logout on token expiration
   - Provide clear error messages
   - Allow users to refresh tokens

4. **Validate User State**
   - Check if user is active
   - Handle deleted users gracefully
   - Validate permissions on each request

5. **Log Authentication Events**
   - Log successful and failed login attempts
   - Monitor for suspicious activity
   - Implement rate limiting

🔧 Common Patterns
==================

Automatic Logout on Token Expiration
------------------------------------

.. code-block:: javascript

    // Axios interceptor for handling expired tokens
    import axios from 'axios';

    axios.interceptors.response.use(
        (response) => response,
        (error) => {
            if (error.response && error.response.status === 401) {
                // Token expired or invalid
                localStorage.removeItem('auth_token');
                window.location.href = '/login';
            }
            return Promise.reject(error);
        }
    );

Rate Limiting
-------------

.. code-block:: python

    # Install: pip install django-ratelimit
    from django_ratelimit.decorators import ratelimit
    from django.utils.decorators import method_decorator

    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST'), name='post')
    class APILoginView(APIView):
        """Login view with rate limiting."""
        pass

🌟 Our Todo App Authentication Flow
===================================

Complete Flow Summary
--------------------

1. **User Registration** (if needed)
2. **Login Request** → Username/Password → API
3. **Token Generation** → Return token to client
4. **Token Storage** → Client stores in localStorage
5. **API Requests** → Include token in Authorization header
6. **Token Validation** → Server validates on each request
7. **Logout** → Delete token from server and client

This provides secure, stateless authentication perfect for our React frontend and Django API backend.

📖 Next Steps
=============

1. 🛡️ **Permissions**: Control access with `Permissions <./05-permissions.rst>`_

🔗 Resources
============

* 📚 `DRF Authentication <https://www.django-rest-framework.org/api-guide/authentication/>`_
* 🎫 `Token Authentication <https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication>`_
* 🔒 `Django Authentication <https://docs.djangoproject.com/en/stable/topics/auth/>`_

---

Authentication is the foundation of API security. With proper token-based authentication, your API can securely serve multiple client types! 🔐

Ready to control what users can do? Let's explore `Permissions <./05-permissions.rst>`_ next!