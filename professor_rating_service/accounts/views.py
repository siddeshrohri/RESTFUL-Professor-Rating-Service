from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def LoginAPI(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    if not username or not password:
        return JsonResponse({'error': 'Username and password are required for Login.'}, status=400)
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        if user.is_superuser:
            return JsonResponse({'error': 'Admin login only allowed via /admin/login/ on localhost'}, status=403)
        else:
            login(request, user)
            return JsonResponse({'message': 'Login successful', 'redirect': 'professor_list'})
    else:
        return JsonResponse({'error': 'Invalid username or password'}, status=401)

@csrf_exempt
def LogoutAPI(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})

@csrf_exempt
def RegisterAPI(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    
    if not username or not email or not password or not confirm_password:
        return JsonResponse({'error': 'All fields are required.'}, status=400)
    
    if password != confirm_password:
        return JsonResponse({'error': 'Passwords do not match!'}, status=400)
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username is already taken!'}, status=400)
    
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Email is already registered!'}, status=400)
    
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.save()
        login(request, user)
        return JsonResponse({'message': 'Registration successful'})
    except Exception as e:
        return JsonResponse({'error': 'An error occurred during registration.'}, status=500)
