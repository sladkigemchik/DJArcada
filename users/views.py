from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.utils import timezone
from .models import User
from .forms import ProfileUserForm, UserRegistrationForm

# Проверки для разных ролей
def is_moderator_or_admin(user):
    return user.is_authenticated and user.role in ['moderator', 'admin']

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

class LoginUser(LoginView):
    template_name = 'users/login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        
        if user.is_banned:
            messages.error(self.request, f'Ваш аккаунт забанен. Причина: {user.ban_reason}')
            return redirect('users:login')
        
        return super().form_valid(form)

class RegisterUser(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        form.instance.role = 'user'
        return super().form_valid(form)
from django.contrib.auth.mixins import LoginRequiredMixin
class ProfileUser(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    
    def get_object(self, queryset=None):
        return self.request.user

class UserPasswordChange(PasswordChangeView):
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:profile')

# Управление банами
@user_passes_test(is_moderator_or_admin)
def user_list_for_moderation(request):
    users = User.objects.all().exclude(role='admin')
    return render(request, 'users/user_list.html', {'users': users})

@user_passes_test(is_moderator_or_admin)
def ban_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        
        if user.role == 'admin':
            messages.error(request, 'Нельзя забанить администратора!')
            return redirect('users:user_list')
        
        if user.role == 'moderator' and request.user.role == 'moderator':
            messages.error(request, 'Модератор не может банить другого модератора!')
            return redirect('users:user_list')
        
        user.is_banned = True
        user.ban_reason = request.POST.get('ban_reason', '')
        user.banned_at = timezone.now()
        user.save()
        
        messages.success(request, f'Пользователь {user.username} забанен!')
    
    return redirect('users:user_list')

@user_passes_test(is_moderator_or_admin)
def unban_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_banned = False
    user.ban_reason = ''
    user.banned_at = None
    user.save()
    
    messages.success(request, f'Пользователь {user.username} разбанен!')
    return redirect('users:user_list')