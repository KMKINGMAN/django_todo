"""
Todo application models.

This module contains the Django model definitions for the Todo application.
"""

from django.contrib.auth.models import User
from django.db import models


def get_default_tags():
    """Return default tags for Todo model."""
    return ["general"]


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
        default=get_default_tags
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

