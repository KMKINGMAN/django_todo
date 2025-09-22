"""
Todo application model.

This module contains the Django model definitions for the Todo application.
"""

from django.contrib.auth.models import User
from django.db import models


def get_default_tags():
    """Return default tags for Todo model."""
    return ["general"]


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
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="todos", null=True, blank=True
    )
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        related_name="todos",
        null=True,
        blank=True,
        help_text="Task this todo belongs to (optional)",
    )
    tags = models.JSONField(blank=True, null=True, default=get_default_tags)

    class Meta:
        """Meta options for Todo model."""

        ordering = ["-created_at"]
        verbose_name = "Todo"
        verbose_name_plural = "Todos"

    def __str__(self):
        """Return string representation of Todo."""
        if self.title and len(self.title) > 50:
            return f"{self.title[:50]}..."
        return self.title or ""

    def __repr__(self):
        """Return detailed string representation for debugging."""
        username = self.user.username if self.user else None
        return (
            f"Todo(id={self.id}, title='{self.title}', "
            f"completed={self.completed}, user={username})"
        )
