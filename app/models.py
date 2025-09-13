"""
Todo application models.

This module contains the Django model definitions for the Todo application.
"""

from django.contrib.auth.models import User
from django.db import models


class Todo(models.Model):
    """
    Todo model representing a task item.
    
    Attributes:
        title: The title/name of the todo item
        description: Optional detailed description
        completed: Boolean flag indicating completion status
        due_date: Optional deadline for the todo
        created_at: Timestamp when todo was created
        updated_at: Timestamp when todo was last modified
        user: Many-to-many relationship with User model
        tags: JSON field containing list of tag strings
    """
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ManyToManyField(
        User, 
        related_name='todos', 
        blank=True
    )
    tags = models.JSONField(
        blank=True, 
        null=True, 
        default=lambda: ["general"]
    )

    class Meta:
        """Meta options for Todo model."""
        ordering = ['-created_at']
        verbose_name = 'Todo'
        verbose_name_plural = 'Todos'

    def __str__(self):
        """Return string representation of Todo."""
        if len(self.title) > 50:
            return f"{self.title[:50]}..."
        return self.title

    def __repr__(self):
        """Return detailed string representation for debugging."""
        return (
            f"Todo(id={self.id}, title='{self.title}', "
            f"completed={self.completed})"
        )

