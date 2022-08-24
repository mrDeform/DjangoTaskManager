from django.urls import path, include
from .views import *

urlpatterns = [
    path('', about, name='about'),
    path('', include('django.contrib.auth.urls')),
    path('index/', index, name='index'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('add_task/', add_task, name='add_task'),
    path('delete_task/', delete_task, name='delete_task'),
    path('update_task/', update_task, name='update_task'),
    path('send_mail/', send_todo_to_email, name='send_todo_to_email'),
]
