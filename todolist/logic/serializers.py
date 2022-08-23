from rest_framework import serializers
from .models import Task, ToDo


class TaskSerializer(serializers.ModelSerializer):
    manager = serializers.CharField(default=serializers.CurrentUserDefault)

    class Meta:
        model = Task
        fields = "__all__"


class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = "__all__"
