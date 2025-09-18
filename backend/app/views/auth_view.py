"""
Authentication views for the Todo application.

This module contains Django REST Framework views for authentication functionality
including login and token management.
"""

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class LoginView(APIView):
    """API view for user authentication and token generation."""

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
                token, _ = Token.objects.get_or_create(user=user)  # pylint: disable=no-member
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
