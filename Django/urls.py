"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

from command import views as command_views


router = routers.DefaultRouter()
# router.register(r'nodes', command_views.NodeInfoViewSet)
# router.register(r'client', command_views.ClientInfoViewSet)

urlpatterns = [
    # path('admin/', admin.site.urls),
    # url(r'^', views.index)
    # url(r'^command/$',command_views.execute_command),
    # url(r'^index/$', command_views.index),

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'command',command_views.general_command)
]
