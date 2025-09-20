"""
Factory classes for creating test data.

This module provides factory classes for creating test instances
of models used in the Todo application testing.
"""
import factory

from django.contrib.auth.models import User
from app.models import Todo, Task


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating User instances for testing."""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True
    is_staff = False
    is_superuser = False


class SuperUserFactory(UserFactory):
    """Factory for creating superuser instances for testing."""

    is_staff = True
    is_superuser = True
    username = factory.Sequence(lambda n: f"admin{n}")


class TaskFactory(factory.django.DjangoModelFactory):
    """Factory for creating Task instances for testing."""

    class Meta:
        model = Task

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph", nb_sentences=2)
    user = factory.SubFactory(UserFactory)


class TodoFactory(factory.django.DjangoModelFactory):
    """Factory for creating Todo instances for testing."""

    class Meta:
        model = Todo

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph", nb_sentences=1)
    completed = False
    user = factory.SubFactory(UserFactory)
    task = factory.SubFactory(TaskFactory)
    tags = factory.LazyFunction(lambda: ["test", "factory"])


class TodoWithoutTaskFactory(TodoFactory):
    """Factory for creating Todo instances without associated Task."""

    task = None
    tags = factory.LazyFunction(lambda: ["standalone", "todo"])


class CompletedTodoFactory(TodoFactory):
    """Factory for creating completed Todo instances."""

    completed = True
    tags = factory.LazyFunction(lambda: ["completed", "done"])
