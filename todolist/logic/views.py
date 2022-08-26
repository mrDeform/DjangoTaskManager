import logging
from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .forms import RegisterUserForm
from .models import Task, ToDo
from .serializers import TaskSerializer, ToDoSerializer
from .permissions import IsAdminOrManager, IsAdminOrManagerOrResponsible

logger = logging.getLogger(__name__)


class RegisterUser(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': RegisterUserForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('about')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


@csrf_exempt
def index(request):
    if request.method == "GET":
        tasks = Task.objects.all()
        return render(request, "todolist/index.html", {"tasks": tasks})
    elif request.method == "POST":
        return redirect('add_task')


def about(request):
    return render(request, "todolist/about.html")


@csrf_exempt
def add_task(request):
    if request.method == "GET":
        return render(request, "todolist/create_task.html")

    elif request.method == "POST":
        data = request.POST

        if data["deadline"]:
            deadline = data["deadline"]
        else:
            deadline = '2050-01-01'

        Task(
            title=data["title"],
            task_description=data["task_description"],
            deadline=deadline,
            manager=request.user,
        ).save()
        return redirect('index')


@csrf_exempt
def delete_task(request):
    id_t = request.GET["id"]
    task = Task(id=id_t)

    logger.info(f'Пользователь {request.user} удалил Task "id"={id_t} title={task.title}')

    task.delete()
    return redirect('index')


@csrf_exempt
def update_task(request):
    if request.method == "GET":
        task_id = request.GET.get('id')
        task = Task.objects.get(id=task_id)
        return render(request, "todolist/update_task.html", {"task": task})

    elif request.method == "POST":
        logger.info(f'Пользователь {request.user} изменил "id"={request.POST["task_id"]} '
                    f'"title"={Task.objects.get(id=request.POST["task_id"]).title}')

        if request.POST["deadline"]:
            deadline = request.POST["deadline"]
        else:
            deadline = '2050-01-01'

        task_upd = Task.objects.get(id=request.POST["task_id"])
        task_upd.title = request.POST["title"]
        task_upd.task_description = request.POST["task_description"]
        task_upd.deadline = deadline
        task_upd.save()
        return redirect('index')


@csrf_exempt
def add_todo(request):
    if request.method == "GET":
        task_id = request.GET.get('id')
        users = User.objects.all()
        return render(request, "todolist/create_todo.html", {"task_id": task_id, 'users': users})
    elif request.method == "POST":
        data = request.POST
        if data["responsible"] == '':
            responsible = None
        else:
            responsible = User.objects.get(id=data["responsible"])
        if data["deadline"]:
            deadline = data["deadline"]
        else:
            deadline = '2050-01-01'

        ToDo(title=data["title"],
             todo_description=data["todo_description"],
             deadline=deadline,
             is_complete=False,
             task=Task.objects.get(id=data["task_id"]),
             responsible=responsible
             ).save()
        return redirect('index')


@csrf_exempt
def update_todo(request):
    if request.method == "GET":
        todo_id = request.GET.get('id')
        todo = ToDo.objects.get(id=todo_id)
        users = User.objects.all()
        return render(request, "todolist/update_todo.html", {"todo": todo, 'users': users})

    elif request.method == "POST":

        if request.POST["responsible"] == '':
            responsible = None
        else:
            responsible = User.objects.get(id=request.POST["responsible"])

        if request.POST["deadline"]:
            deadline = request.POST["deadline"]
        else:
            deadline = '2050-01-01'

        try:
            complete = request.POST["is_complete"]
        except:
            complete = False
        logger.info(f'Пользователь {request.user} изменил "id"={request.POST["todo_id"]} "title"={ToDo.objects.get(id=request.POST ["todo_id"]).title}')
        todo_upd = ToDo.objects.get(id=request.POST["todo_id"])
        todo_upd.title = request.POST["title"]
        todo_upd.todo_description = request.POST["todo_description"]
        todo_upd.deadline = deadline
        todo_upd.is_complete = complete
        todo_upd.responsible = responsible
        todo_upd.save()
        return redirect('index')


@csrf_exempt
def delete_todo(request):
    logger.info(f'Пользователь {request.user} удалил ToDo "id"={request.GET["id"]} '
                f'"title"={ToDo.objects.get(id=request.GET["id"]).title}')

    ToDo(id=request.GET["id"]).delete()
    return redirect('index')


class TaskAPIList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)


class TaskAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAdminOrManager,)


class TaskAPIDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAdminOrManager,)


class TodoAPIList(generics.ListCreateAPIView):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    permission_classes = (IsAuthenticated,)


class TodoAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    permission_classes = (IsAdminOrManagerOrResponsible,)


class TodoAPIDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    permission_classes = (IsAdminOrManagerOrResponsible,)


@csrf_exempt
def send_todo_to_email(request):
    if request.method == "GET":
        to_do = ToDo.objects.get(id=request.GET["id"])
        responsible_email = to_do.responsible.email
        mail = send_mail(subject='Вам задание №{}'.format(to_do.id),
                         message='Добрый день\nВам выдано задание: {0}.\nОписание: {1}.'.format(to_do.title, to_do.todo_description),
                         from_email='necht0_0@mail.ru',
                         recipient_list=[responsible_email],
                         fail_silently=False)
        try:
            if mail:
                message = 'Письмо успешно отправлено'
                return render(request, "todolist/mail.html", {"message": message})
            else:
                message = 'Ошибка отправки письма'
                return render(request, "todolist/mail.html", {"message": message})
        except:
            message = 'Ошибка данных'
            return render(request, "todolist/mail.html", {"message": message})
    else:
        message = 'Метод не определен'
        return render(request, "todolist/mail.html", {"message": message})
