from django.contrib import admin
from .models import Todo
from .views import TodoViewSet

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'completed', 'due_date', 'created_at', 'updated_at', 'tags', 'description')
	list_filter = ('completed', 'tags', 'user', 'created_at', 'updated_at')
	search_fields = ('title', 'description', 'tags')
