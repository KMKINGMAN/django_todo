"""
Configuration for pytest and Django testing.

This module contains pytest fixtures and configurations
that are shared across all test modules.
"""

import pytest
from django.contrib.auth.models import User
from django.test import Client
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def client():
    """Provide a Django test client."""
    return Client()


@pytest.fixture
def api_client():
    """Provide a DRF API test client."""
    return APIClient()


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )


@pytest.fixture
def superuser(db):
    """Create a test superuser."""
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpass123"
    )


@pytest.fixture
def user_token(user):
    """Create an authentication token for the test user."""
    token, created = Token.objects.get_or_create(user=user)
    return token


@pytest.fixture
def authenticated_client(api_client, user_token):
    """Provide an authenticated API client."""
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
    return api_client


@pytest.fixture
def superuser_token(superuser):
    """Create an authentication token for the test superuser."""
    token, created = Token.objects.get_or_create(user=superuser)
    return token


@pytest.fixture
def authenticated_superuser_client(api_client, superuser_token):
    """Provide an authenticated superuser API client."""
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {superuser_token.key}')
    return api_client
