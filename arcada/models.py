from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User   


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=GameArticle.Status.PUBLISHED)


class GameArticle(models.Model):
    tags = models.ManyToManyField('TagPost', blank=True, related_name='articles')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, related_name='articles')
    
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"
    
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Содержание")
    
    game_name = models.CharField(max_length=255, verbose_name="Название игры")
    genre = models.CharField(max_length=100, blank=True, verbose_name="Жанр")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена")
    
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    status = models.IntegerField(choices=Status.choices, default=Status.DRAFT, verbose_name="Статус")
    
    objects = models.Manager()           
    published = PublishedManager()       
    
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


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name="Тег")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, verbose_name="О себе")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    
    def __str__(self):
        return f"Профиль {self.user.username}"