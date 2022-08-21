from django.contrib import admin
from .models import Task, ToDo

admin.site.register(ToDo)
admin.site.register(Task)
