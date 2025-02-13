# professors_rating/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def professor_list(request):
    # Hardcoding the list of professors
    professors = [
        {'name': 'Professor A', 'department': 'Computer Science'},
        {'name': 'Professor B', 'department': 'Mathematics'},
        {'name': 'Professor C', 'department': 'Physics'},
        {'name': 'Professor D', 'department': 'Chemistry'},
    ]
    
    return render(request, 'professor_rating/professor_list.html', {'professors': professors})
def home(request):
    # if not request.user.is_authenticated:
    #     return render(request, 'home.html')  
    return redirect('/accounts/login/')
