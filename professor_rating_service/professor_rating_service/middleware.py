from django.shortcuts import redirect
from django.conf import settings

class LoginRequiredMiddleware:
    """Middleware to require login for all views except login/register."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = [settings.LOGIN_URL, '/accounts/register/', '/admin/']  # Allow login, register, and admin
        if not request.user.is_authenticated and request.path not in allowed_paths:
            return redirect(settings.LOGIN_URL)
        return self.get_response(request)
