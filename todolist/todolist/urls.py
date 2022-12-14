"""todolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf import settings
# from rest_framework import routers
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from logic.views import *

# router = routers.DefaultRouter()
# router.register(r'task', TaskViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('logic.urls')),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    # path('api/v1/', include(router.urls))
    path('api/v1/task/', TaskAPIList.as_view()),
    path('api/v1/task/<int:pk>/', TaskAPIUpdate.as_view()),
    path('api/v1/task/<int:pk>/', TaskAPIDestroy.as_view()),
    path('api/v1/todo/', TodoAPIList.as_view()),
    path('api/v1/todo/<int:pk>/', TodoAPIUpdate.as_view()),
    path('api/v1/todo/<int:pk>/', TodoAPIDestroy.as_view()),
]
