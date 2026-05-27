from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('article/<slug:article_slug>/', views.article_detail, name='article_detail'),
    path('category/<slug:cat_slug>/', views.category, name='category'),
    path('tag/<slug:tag_slug>/', views.tag, name='tag'),
    path('add/', views.add_game, name='add_game'),
    
    # Новые URL для модерации
    path('pending/', views.pending_articles, name='pending_articles'),
    path('approve/<int:article_id>/', views.approve_article, name='approve_article'),
    path('reject/<int:article_id>/', views.reject_article, name='reject_article'),
    
    path('ai/ask/', views.ask_yandex_gpt, name='ask_gpt'),
    path('ai/', views.ai_chat, name='ai_chat'),
    path('search/', views.search, name='search'),
    path('edit/<int:article_id>/', views.edit_article, name='edit_article'),
    path('delete/<int:article_id>/', views.delete_article, name='delete_article'),
]