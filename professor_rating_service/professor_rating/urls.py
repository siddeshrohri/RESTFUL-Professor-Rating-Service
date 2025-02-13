# professors_rating/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.professor_list, name='professor_list'),
]
