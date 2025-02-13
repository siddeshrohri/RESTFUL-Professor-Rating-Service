from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect admin users to Django's admin panel
            if user.is_superuser:
                return redirect('/admin/')

            # Redirect normal users to professor list
            return redirect('professor_list')

        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'accounts/login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Registration View
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.save()

        login(request, user)  # Automatically log in the user after registration
        return redirect('professor_list')

    return render(request, 'accounts/register.html')

# Redirect Home to Login if Not Authenticated
# def home(request):
#     if not request.user.is_authenticated:
#         return redirect('login')  # Always redirect to login page
#     return redirect('professor_list')  # Redirect authenticated users to the professor list
