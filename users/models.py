from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Пользователь'),
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Роль'
    )
    
    is_banned = models.BooleanField(default=False, verbose_name='Забанен')
    ban_reason = models.TextField(blank=True, null=True, verbose_name='Причина бана')
    banned_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата бана')
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_moderator(self):
        return self.role == 'moderator'
    
    def is_user(self):
        return self.role == 'user'
    
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"