from django.urls import path
from . import views

urlpatterns = [
    path('', views.professor_list, name='professor_list'),
    # Updated to include both professor_id and module_code in the URL
    path('rate/<str:professor_id>/<str:module_code>/', views.rate_professor, name='rate_professor'),
    path('view/', views.view_ratings, name='view_ratings'),
    # Updated to include both professor_id and module_code in the URL
    path('average/<str:professor_id>/<str:module_code>/', views.average_rating, name='average_rating'),
]
