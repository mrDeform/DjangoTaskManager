from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField('Название задачи', max_length=500)
    task_description = models.CharField('Описание задачи', max_length=2000)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateField('Дата добавления', auto_now_add=True)
    deadline = models.DateField('Срок выполнения')

    def __str__(self):
        return self.title


# class ToDo(models.Model):
#     title = models.CharField('Название задания', max_length=500)
#     not_main = models.BooleanField('Дочернее задание', default=False)
#     is_complete = models.BooleanField('Завершено', default=False)
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.title

