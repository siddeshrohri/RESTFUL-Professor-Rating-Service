from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginAPI, name="login"),
    path("logout/", views.LogoutAPI, name="logout"),
    path("register/", views.RegisterAPI, name="register"),
]
