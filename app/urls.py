from rest_framework import routers
from django.urls import path, include
from .views import TodoViewSet

router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')

urlpatterns = [
    path('', include(router.urls)),
]
