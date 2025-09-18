
"""
Todo application views for Todo.

This module contains Django REST Framework views for the Todo model.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Todo
from ..serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """ViewSet for managing Todo instances via REST API."""

    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return todos filtered by current user or all for superuser."""
        if self.request.user.is_superuser:
            return Todo.objects.all().order_by('-created_at')  # pylint: disable=no-member
        return Todo.objects.filter(  # pylint: disable=no-member
            user=self.request.user
        ).order_by('-created_at')

    def perform_create(self, serializer):
        """Associate created todo with current user."""
        serializer.save(user=self.request.user)


@login_required
def dashboard(request):
    """Render the dashboard template for authenticated users."""
    return render(request, 'dashboard.html', {'user': request.user})
