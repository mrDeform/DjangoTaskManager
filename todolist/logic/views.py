from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from .serializers import TaskSerializer, ToDoSerializer
from .models import Task, ToDo


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


class TodoViewSet(viewsets.ModelViewSet):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer


@csrf_exempt
def send_todo_to_email(request):
    if request.method == "GET":
        to_do = ToDo.objects.get(id=request.GET["todo_id"])
        responsible_email = to_do.responsible.email
        mail = send_mail(subject='Вам задание №{}'.format(to_do.id),
                         message='Задание: {0}.\nОписание: {1}.'.format(to_do.title, to_do.todo_description),
                         from_email='necht0_0@mail.ru',
                         recipient_list=[responsible_email],
                         fail_silently=False)
        try:
            if mail:
                return HttpResponse('<div><br><br><h2>Письмо успешно отправлено</h2><br></div>')
            else:
                return HttpResponse('<div><br><br><h2>Ошибка отправки письма</h2><br></div>')
        except:
            return HttpResponse('<div><br><br><h2>Ошибка данных</h2><br></div>')
    else:
        return HttpResponse('<div><br><br><h2>Метод не определен</h2><br><h3>Данный метод не назначен</h3></div>')
