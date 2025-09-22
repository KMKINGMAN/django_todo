
"""
Todo application views.

This module contains Django REST Framework views and
serializers for the Todo model.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Task
from ..serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """ViewSet for managing Task instances via REST API."""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        """Include request and an explicit include_todos flag from query params.

        Passing include_todos here keeps request-specific logic in the view
        and allows the serializer to avoid querying/serializing todos when not
        requested by the client.

        resources:
            https://www.django-rest-framework.org/api-guide/requests/#query_params
            https://www.django-rest-framework.org/api-guide/serializers/#including-extra-context

        """
        context = super().get_serializer_context()
        include = self.request.query_params.get('include_todos') == '1'
        context['include_todos'] = include
        return context

    def get_queryset(self):
        """Return tasks filtered by current user or all for superuser."""
        if self.request.user.is_superuser:
            return Task.objects.prefetch_related(
                'todos').all().order_by('-created_at')
        return Task.objects.filter(user=self.request.user).prefetch_related(
            'todos').order_by('-created_at')

    def perform_create(self, serializer):
        """Associate created task with current user.

        resources:
            https://www.cdrf.co/3.16/rest_framework.viewsets/ModelViewSet.html#perform_create
        """
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        """Delete task and all related todos owned by the user.
        resources:
            https://www.cdrf.co/3.16/rest_framework.viewsets/ModelViewSet.html#perform_destroy
        """
        if self.request.user.is_superuser:
            instance.todos.all().delete()
        else:
            instance.todos.filter(user=self.request.user).delete()
        instance.delete()
