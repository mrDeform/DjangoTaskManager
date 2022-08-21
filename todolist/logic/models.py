from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField('Название задачи', max_length=500)
    task_description = models.CharField('Описание задачи', max_length=2000)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    date_add = models.DateTimeField('Дата добавления', auto_now_add=True)
    date_update = models.DateTimeField('Дата изменения', auto_now=True)
    deadline = models.DateField('Срок выполнения')
    is_complete = models.BooleanField('Завершено', default=False)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title


class ToDo(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField('Название задания', max_length=500)
    todo_description = models.CharField('Описание задания', max_length=4000)
    parent_todo = models.IntegerField('Родительское задание', default=0)
    date_add = models.DateTimeField('Дата добавления', auto_now_add=True)
    date_update = models.DateTimeField('Дата изменения', auto_now=True)
    deadline = models.DateField('Срок выполнения')
    is_complete = models.BooleanField('Завершено', default=False)

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return self.title

