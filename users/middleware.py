from django.shortcuts import redirect

class BanMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_banned:
            if not request.path.startswith('/users/logout/'):
                return redirect('users:logout')
        return self.get_response(request)