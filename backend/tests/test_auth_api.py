"""
API tests for authentication endpoints.

This module contains comprehensive tests for the authentication
API endpoints including login functionality.
"""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
@pytest.mark.api
class TestAuthenticationAPI:
    """Test cases for authentication API endpoints."""

    def test_login_with_valid_credentials(self, api_client):
        """Test successful login with valid credentials."""
        # Create a test user
        user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        
        # Login data
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        
        # Make login request
        url = reverse('api_login')
        response = api_client.post(url, login_data, format='json')
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data
        assert 'user_id' in response.data
        assert 'username' in response.data
        assert response.data['user_id'] == user.id
        assert response.data['username'] == user.username
        
        # Verify token was created
        token = Token.objects.get(user=user)
        assert response.data['token'] == token.key

    def test_login_with_invalid_credentials(self, api_client):
        """Test login failure with invalid credentials."""
        # Create a test user
        User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        
        # Login with wrong password
        login_data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        
        url = reverse('api_login')
        response = api_client.post(url, login_data, format='json')
        
        # Assertions
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'error' in response.data
        assert response.data['error'] == 'Invalid credentials'

    def test_login_with_nonexistent_user(self, api_client):
        """Test login failure with non-existent user."""
        login_data = {
            "username": "nonexistent",
            "password": "password123"
        }
        
        url = reverse('api_login')
        response = api_client.post(url, login_data, format='json')
        
        # Assertions
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'error' in response.data
        assert response.data['error'] == 'Invalid credentials'

    def test_login_with_missing_username(self, api_client):
        """Test login failure with missing username."""
        login_data = {
            "password": "testpass123"
        }
        
        url = reverse('api_login')
        response = api_client.post(url, login_data, format='json')
        
        # Assertions
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert response.data['error'] == 'Username and password required'

    def test_login_with_missing_password(self, api_client):
        """Test login failure with missing password."""
        login_data = {
            "username": "testuser"
        }
        
        url = reverse('api_login')
        response = api_client.post(url, login_data, format='json')
        
        # Assertions
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert response.data['error'] == 'Username and password required'

    def test_login_with_empty_data(self, api_client):
        """Test login failure with empty data."""
        url = reverse('api_login')
        response = api_client.post(url, {}, format='json')
        
        # Assertions
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert response.data['error'] == 'Username and password required'

    def test_login_get_method_not_allowed(self, api_client):
        """Test that GET method is not allowed for login endpoint."""
        url = reverse('api_login')
        response = api_client.get(url)
        
        # Assertions
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_existing_token_reused_on_login(self, api_client):
        """Test that existing token is reused when user logs in again."""
        # Create a test user
        user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        
        # Create an existing token
        existing_token = Token.objects.create(user=user)
        
        # Login data
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        
        # Make login request
        url = reverse('api_login')
        response = api_client.post(url, login_data, format='json')
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        assert response.data['token'] == existing_token.key
        
        # Verify only one token exists for the user
        assert Token.objects.filter(user=user).count() == 1
