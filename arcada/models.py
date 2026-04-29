from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    """Менеджер для получения только опубликованных статей"""
    def get_queryset(self):
        return super().get_queryset().filter(status=GameArticle.Status.PUBLISHED)


class GameArticle(models.Model):
    """Модель для хранения статей об играх"""
    
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"
    
    # Основные поля
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Содержание")
    
    # Игровые поля
    game_name = models.CharField(max_length=255, verbose_name="Название игры")
    genre = models.CharField(max_length=100, blank=True, verbose_name="Жанр")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена")
    
    # Служебные поля
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    status = models.IntegerField(choices=Status.choices, default=Status.DRAFT, verbose_name="Статус")
    
    # Менеджеры
    objects = models.Manager()           # все записи
    published = PublishedManager()       # только опубликованные
    
    class Meta:
        ordering = ["-time_create"]
        indexes = [
            models.Index(fields=["-time_create"]),
            models.Index(fields=["status"]),
        ]
        verbose_name = "Игровая статья"
        verbose_name_plural = "Игровые статьи"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'article_slug': self.slug})