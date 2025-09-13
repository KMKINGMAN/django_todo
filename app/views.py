
from rest_framework import viewsets
from rest_framework import serializers as drf_serializers
from .models import Todo
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework.request import Request
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def todo(request: Request):
	if request.method == 'GET':
		todos = Todo.objects.filter(user=request.user).order_by('-created_at')
		serializer = TodoSerializer(todos, many=True)
		return Response(serializer.data)
	elif request.method == 'POST':
		serializer = TodoSerializer(data=request.data)
		if serializer.is_valid():
			todo_instance = serializer.save()
			todo_instance.user.add(request.user)
			return Response(serializer.data, status=201)
		return Response(serializer.errors, status=400)
	elif request.method == 'PATCH':
		todo_id = request.data.get('id')
		if not todo_id:
			return Response({'error': 'ID is required for PATCH'}, status=400)
		try:
			todo_instance = Todo.objects.get(id=todo_id)
		except Todo.DoesNotExist:
			return Response({'error': 'Todo not found'}, status=404)
		serializer = TodoSerializer(todo_instance, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=400)
	elif request.method == 'DELETE':
		todo_id = request.data.get('id')
		if not todo_id:
			return Response({'error': 'ID is required for DELETE'}, status=400)
		try:
			todo_instance = Todo.objects.get(id=todo_id)
		except Todo.DoesNotExist:
			return Response({'error': 'Todo not found'}, status=404)
		todo_instance.delete()
		return Response(status=204)


class TodoSerializer(drf_serializers.ModelSerializer):
	user = drf_serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)
	tags = drf_serializers.ListField(child=drf_serializers.CharField(), required=False)

	class Meta:
		model = Todo
		fields = ['id', 'title', 'completed', 'created_at', 'description', 'due_date', 'updated_at', 'user', 'tags']

	def create(self, validated_data):
		users = validated_data.pop('user', [])
		tags = validated_data.pop('tags', None)
		todo = Todo.objects.create(**validated_data)
		if users:
			todo.user.set(users)
		if tags is not None:
			todo.tags = tags
			todo.save()
		return todo


class TodoViewSet(viewsets.ModelViewSet):
	serializer_class = TodoSerializer
	permission_classes = [IsAuthenticated]
	
	def get_queryset(self):
		return Todo.objects.filter(user=self.request.user).order_by('-created_at')
	
	def perform_create(self, serializer):
		todo = serializer.save()
		todo.user.add(self.request.user)


@login_required
def dashboard(request):
	return render(request, 'dashboard.html', {'user': request.user})
