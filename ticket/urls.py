"""Ticket_Complaint_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from unicodedata import name
from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
path("index/",views.index,name="index"),
path("move_to_inprogress/",views.move_to_inprogress, name="move_to_inprogress"),
path("move_to_done/",views.move_to_done, name="move_to_done"),
path("create_comment/",views.create_comment, name="create_comment"),
]
