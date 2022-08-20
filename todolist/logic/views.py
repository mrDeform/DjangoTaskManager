from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from .serializers import TaskSerializer
from .models import Task


@csrf_exempt
def index(request):
    if request.method == "GET":
        tasks = Task.objects.all()
        return render(request, "todolist/index.html", {"tasks": tasks})
    elif request.method == "POST":
        return redirect('add_task')


@csrf_exempt
def add_task(request):
    if request.method == "GET":
        return render(request, "todolist/create_task.html")
    elif request.method == "POST":
        Task(
            title=request.POST["title"],
            task_description=request.POST["task_description"],
            manager=User.objects.get(id=request.POST["manager_id"]),
            deadline=request.POST["deadline"],
        ).save()
        return redirect('index')


@csrf_exempt
def delete_task(request):
    if request.method == "GET":
        return render(request, "todolist/delete_task.html")
    elif request.method == "POST":
        Task(
            id=request.POST["delete_id"],
        ).delete()
        return redirect('index')


@csrf_exempt
def update_task(request):
    if request.method == "GET":
        return render(request, "todolist/update_task.html")
    elif request.method == "POST":
        task_upd = Task.objects.get(id=request.POST["task_id"])
        task_upd.title = request.POST["title"]
        task_upd.task_description = request.POST["task_description"]
        task_upd.deadline = request.POST["deadline"]
        task_upd.save()
        return redirect('index')


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
