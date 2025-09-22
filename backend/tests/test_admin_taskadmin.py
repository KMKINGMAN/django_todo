"""Tests for TaskAdmin admin behavior."""

import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User

from app.admin import TaskAdmin
from app.models import Task, Todo

pytestmark = pytest.mark.django_db


class DummyRequest:
    """Minimal request object with a user attribute for admin methods."""

    def __init__(self, user):
        self.user = user


def test_taskadmin_get_queryset_filters_and_annotates():
    admin_site = AdminSite()
    admin = TaskAdmin(Task, admin_site)

    user1 = User.objects.create_user(username="u1", password="pw")
    _ = User.objects.create_user(username="u2", password="pw")
    t1 = Task.objects.create(title="T1", user=user1)
    t2 = Task.objects.create(title="T2", user=user1)  # pylint: disable=unused-variable
    Todo.objects.create(title="A", user=user1, task=t1)
    Todo.objects.create(title="B", user=user1, task=t1)

    # Superuser sees all
    su = User.objects.create_superuser(username="admin", password="pw", email="a@b.com")
    qs_all = admin.get_queryset(DummyRequest(su))
    assert qs_all.count() >= 2
    # Non-superuser sees only their tasks
    qs_user1 = admin.get_queryset(DummyRequest(user1))
    assert qs_user1.count() == 2
    # Annotated _todos_count present on objects
    obj = qs_user1.first()
    assert hasattr(obj, "_todos_count")


def test_formfield_for_foreignkey_limits_non_superuser():
    admin_site = AdminSite()
    admin = TaskAdmin(Task, admin_site)
    user = User.objects.create_user(username="u3", password="pw")

    # Use the real model field instance so Django's admin machinery can
    # call .formfield() on it.
    field = Task._meta.get_field("user")
    ff = admin.formfield_for_foreignkey(field, DummyRequest(user))
    # The returned form field should contain a queryset limited to current user
    qs = ff.queryset
    assert list(qs) == [user]


def test_save_model_sets_user_for_non_superuser():
    admin_site = AdminSite()
    admin = TaskAdmin(Task, admin_site)
    user = User.objects.create_user(username="u4", password="pw")
    task = Task(title="Unsaved")

    # Simulate save_model call
    admin.save_model(DummyRequest(user), task, form=None, change=False)
    assert task.user == user
