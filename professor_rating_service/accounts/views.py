from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    if not username and not password:
        return JsonResponse({'error': 'Both username and password are required for Login.'}, status=400)
    elif not username:
        return JsonResponse({'error': 'Username is required for Login.'}, status=400)
    elif not password:
        return JsonResponse({'error': 'Password is required for Login.'}, status=400)
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        if user.is_superuser:
            return JsonResponse({'error': 'Admin login only allowed via /admin/login/ on localhost'}, status=403)
        try:
            login(request, user)
        except Exception as e:
            return JsonResponse({'error': 'Error during login process.'}, status=500)
        return JsonResponse({'message': 'Login successful', 'redirect': 'professor_list'})
    else:
        return JsonResponse({'error': 'Invalid username or password'}, status=401)

@csrf_exempt
def logout_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        logout(request)
    except Exception as e:
        return JsonResponse({'error': 'Error during logout process.'}, status=500)
    
    return JsonResponse({'message': 'Logged out successfully'})

@csrf_exempt
def register_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    
    missing_fields = []
    if not username:
        missing_fields.append("username")
    if not email:
        missing_fields.append("email")
    if not password:
        missing_fields.append("password")
    if not confirm_password:
        missing_fields.append("confirm_password")
    
    if missing_fields:
        return JsonResponse(
            {'error': f"The following fields are required: {', '.join(missing_fields)}."}, 
            status=400
        )
    
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
    except Exception as e:
        return JsonResponse({'error': 'An error occurred during registration.'}, status=500)
    
    return JsonResponse({'message': 'Registration successful'})
