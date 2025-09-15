"""
Todo application models.

This module contains the Django model definitions for the Todo application.
"""

from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    """
    Task model representing a collection of todos.
    
    Attributes:
        title: The title/name of the task
        description: Optional detailed description
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last modified
        user: Foreign key to User model (owner of the task)
        todos: Many-to-many relationship with Todo model
    """
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    todos = models.ManyToManyField(
        'Todo',
        related_name='tasks',
        blank=True
    )

    class Meta:
        """Meta options for Task model."""
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        """Return string representation of Task."""
        if len(self.title) > 50:
            return f"{self.title[:50]}..."
        return self.title

    def __repr__(self):
        """Return detailed string representation for debugging."""
        return (
            f"Task(id={self.id}, title='{self.title}', "
            f"user={self.user.username})"
        )
