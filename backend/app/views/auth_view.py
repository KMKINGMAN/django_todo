"""
Authentication views for the Todo application.

This module contains Django REST Framework views
for authentication functionality
including login and token management.
"""

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class LoginView(APIView):
    """API view for user authentication and token generation.
    resources:
        https://www.django-rest-framework.org/api-guide/views/#class-based-views
        https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
        https://www.cdrf.co/3.16/rest_framework.views/APIView.html
    """

    permission_classes = [AllowAny]
    http_method_names = ['post']

    def post(self, request):
        """
        Handle POST request for user login.
        Args:
            request: HTTP request containing username and password
        Returns:
            Response: JSON response with token and user info or error message
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'username': user.username
                })
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            {'error': 'Username and password required'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ValidateTokenView(APIView):
    """API view for token validation."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handle GET request for token validation.
        Args:
            request: HTTP request with Authorization header
        Returns:
            Response: JSON response with user info if token is valid
        """
        return Response({
            'valid': True,
            'user_id': request.user.id,
            'username': request.user.username
        })
