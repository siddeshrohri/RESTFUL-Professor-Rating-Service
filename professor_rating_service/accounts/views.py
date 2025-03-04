# from django.shortcuts import render, redirect
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.models import User
# from django.contrib import messages

# # Login View
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)

#             # Redirect admin users to Django's admin panel
#             if user.is_superuser:
#                 return redirect('/admin/')

#             # Redirect normal users to professor list
#             return redirect('professor_list')

#         else:
#             messages.error(request, 'Invalid username or password')
#             return redirect('login')

#     return render(request, 'accounts/login.html')

# # Logout View
# def logout_view(request):
#     logout(request)
#     return redirect('login')

# # Registration View
# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']

#         if password != confirm_password:
#             messages.error(request, "Passwords do not match!")
#             return redirect('register')

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already taken!")
#             return redirect('register')

#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email is already registered!")
#             return redirect('register')

#         user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
#         user.save()

#         login(request, user)  # Automatically log in the user after registration
#         return redirect('professor_list')

#     return render(request, 'accounts/register.html')

# Redirect Home to Login if Not Authenticated
# def home(request):
#     if not request.user.is_authenticated:
#         return redirect('login')  # Always redirect to login page
#     return redirect('professor_list')  # Redirect authenticated users to the professor list

# from django.http import JsonResponse
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.models import User
# from django.shortcuts import redirect
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             if user.is_superuser:
#                 # Return a JSON response including the redirect URL for admin users
#                 return JsonResponse({'message': 'Admin login successful', 'redirect': '/admin/'})
#             return JsonResponse({'message': 'Login successful'})
#         else:
#             return JsonResponse({'error': 'Invalid username or password'}, status=400)
#     elif request.method == 'GET':
#         if request.user.is_authenticated:
#             if request.user.is_superuser:
#                 return redirect('/admin/')
#             return JsonResponse({'message': 'User already logged in'})
#         return JsonResponse({'error': 'POST method required'}, status=405)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)


# @csrf_exempt
# def logout_view(request):
#     if request.method == 'POST':
#         logout(request)
#         return JsonResponse({'message': 'Logged out successfully'})
#     else:
#         return JsonResponse({'error': 'POST method required'}, status=405)

# @csrf_exempt
# def register(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
        
#         # Check if password and confirm_password match
#         if password != confirm_password:
#             return JsonResponse({'error': 'Passwords do not match!'}, status=400)
        
#         if User.objects.filter(username=username).exists():
#             return JsonResponse({'error': 'Username already taken!'}, status=400)
        
#         if User.objects.filter(email=email).exists():
#             return JsonResponse({'error': 'Email is already registered!'}, status=400)
        
#         user = User.objects.create_user(username=username, email=email, password=password)
#         user.save()
#         login(request, user)  # Automatically log in the user after registration
#         return JsonResponse({'message': 'Registration successful', 'redirect': 'professor_list'})
#     else:
#         return JsonResponse({'error': 'POST method required'}, status=405)



# from django.shortcuts import render, redirect
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.models import User
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib import messages

# @csrf_exempt
# def login_view(request):
#     if request.method == 'GET':
#         # Render the login HTML page for browser access.
#         return render(request, 'accounts/login.html')
    
#     elif request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         # print("DEBUG: Received username:", username, "password:", password)
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             login(request, user)
#             accepts_html = "text/html" in request.META.get("HTTP_ACCEPT", "")
#             if accepts_html:
#                 # Redirect based on user type when HTML is expected.
#                 if user.is_superuser:
#                     return redirect('/admin/')
#                 else:
#                     return redirect('professor_list')
#             else:
#                 # For CLI (JSON) responses, include a redirect key.
#                 if user.is_superuser:
#                     return JsonResponse({'message': 'Admin login successful', 'redirect': '/admin/'})
#                 else:
#                     return JsonResponse({'message': 'Login successful', 'redirect': 'professor_list'})
#         else:
#             if "text/html" in request.META.get("HTTP_ACCEPT", ""):
#                 messages.error(request, 'Invalid username or password')
#                 return redirect('login')
#             else:
#                 return JsonResponse({'error': 'Invalid username or password'}, status=400)
    
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)
# @csrf_exempt
# def logout_view(request):
#     if request.method == 'POST':
#         logout(request)
#         return JsonResponse({'message': 'Logged out successfully'})
#     else:
#         return JsonResponse({'error': 'POST method required'}, status=405)


# @csrf_exempt
# def register(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         first_name = request.POST.get('first_name', '')
#         last_name = request.POST.get('last_name', '')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
        
#         if password != confirm_password:
#             return JsonResponse({'error': 'Passwords do not match!'}, status=400)
#         if User.objects.filter(username=username).exists():
#             return JsonResponse({'error': 'Username already taken!'}, status=400)
#         if User.objects.filter(email=email).exists():
#             return JsonResponse({'error': 'Email is already registered!'}, status=400)
        
#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password,
#             first_name=first_name,
#             last_name=last_name
#         )
#         user.save()
#         login(request, user)
#         return JsonResponse({'message': 'Registration successful'})
#     else:
#         return JsonResponse({'error': 'POST method required'}, status=405)


from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        if user.is_superuser:
            return JsonResponse({'error': 'Admin login only allowed via /admin/login/'}, status=403)
        else:
            login(request, user)
            return JsonResponse({'message': 'Login successful', 'redirect': 'professor_list'})
    else:
        return JsonResponse({'error': 'Invalid username or password'}, status=400)

@csrf_exempt
def logout_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'})
    else:
        return JsonResponse({'error': 'POST method required'}, status=405)

@csrf_exempt
def register(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        # first_name = request.POST.get('first_name', '')
        # last_name = request.POST.get('last_name', '')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match!'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already taken!'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email is already registered!'}, status=400)
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            # first_name=first_name,
            # last_name=last_name
        )
        user.save()
        login(request, user)
        return JsonResponse({'message': 'Registration successful'})
    else:
        return JsonResponse({'error': 'POST method required'}, status=405)
