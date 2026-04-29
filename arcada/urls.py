from django.urls import path
from arcada import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('article/<slug:article_slug>/', views.article_detail, name='article_detail'), 
]

handler404 = views.page_not_found