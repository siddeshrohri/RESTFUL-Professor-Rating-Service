"""
URL configuration for professor_rating_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
# professors_rating_service/urls.py
from django.contrib import admin
from django.urls import path, include
from professor_rating import views  # Import home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Authentication routes
    # path('', views.home, name='home'),  # Home page
    path('professor_rating/', include('professor_rating.urls')),  # Include professor rating app URLs
]
