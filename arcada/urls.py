from django.urls import path
from arcada import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('article/<slug:article_slug>/', views.article_detail, name='article_detail'), 
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_articles, name='tag'),
    path('add/', views.add_game, name='add_game'),
    path('ai/ask/', views.ask_yandex_gpt, name='ask_gpt'),
    path('ai/', views.ai_chat, name='ai_chat'),
]

handler404 = views.page_not_found