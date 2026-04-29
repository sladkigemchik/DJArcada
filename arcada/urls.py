from django.urls import path
from arcada import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
]

handler404 = views.page_not_found