from rest_framework import routers
from django.urls import path, include
from .views import TodoViewSet, my_todos_api

router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')

urlpatterns = [
    path('', include(router.urls)),
    path('my-todos/', my_todos_api, name='my-todos'),
]
