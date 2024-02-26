"""HelloWorld URL Configuration

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

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import staticfiles

from django.contrib import admin
from django.urls import path,include

from django.urls import re_path as url
# from django.conf.urls import url
 
from . import views


 
urlpatterns = [
    path('main/', views.fina),
    path('input/', views.input ,name='input'),
    # path('input/sumbit_ajax/', views.sumbit_ajax),
    path('input/result/', views.result),
    path('progress/result/', views.result),
    path('progress/', views.progress),

]


urlpatterns += staticfiles_urlpatterns()
