from django.db.models import Model, CharField, BooleanField, DateTimeField, TextField, ManyToManyField, JSONField as Json
from django.contrib.auth.models import User



"""
title
description
completed
due_date
created_at
updated_at
user (ManyToMany with User model)
tags (JSONField, default to ["general"])
"""

class Todo(Model):
    title = CharField(max_length=200)
    description = TextField(blank=True, null=True)
    completed = BooleanField(default=False)
    due_date = DateTimeField(blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    user = ManyToManyField(User, related_name='todos', blank=True)
    tags = Json(blank=True, null=True, default=lambda: ["general"])

    def __str__(self) -> str:
        return f"{self.title[:50]}{'...' if len(self.title) > 50 else ''}"

