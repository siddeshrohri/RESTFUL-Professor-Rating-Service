from django.urls import path
from . import views

urlpatterns = [
    path('', views.professor_list, name='professor_list'),
    path('rate/<str:professor_id>/<str:module_code>/', views.rate_professor, name='rate_professor'),
    path('view/', views.view_ratings, name='view_ratings'),
    path('average/<str:professor_id>/<str:module_code>/', views.average_rating, name='average_rating'),
    path('api_rate_professor/', views.api_rate_professor, name='api_rate_professor'),  # <-- Add this line
]
