from django.shortcuts import render
from django.http import HttpResponse

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
]

cats_db = [
    {'id': 1, 'name': 'Экшен'},
    {'id': 2, 'name': 'Стратегии'},
    {'id': 3, 'name': 'RPG'},
]

def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }
    return render(request, 'arcada/index.html', context=data)

def about(request):
    data = {
        'title': 'О сайте',
        'menu': menu,
    }
    return render(request, 'arcada/about.html', context=data)

def page_not_found(request, exception):
    return HttpResponse("<h1>Страница не найдена</h1>")