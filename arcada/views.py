from django.shortcuts import render, get_object_or_404
from arcada.models import GameArticle

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
]

def index(request):
    articles = GameArticle.published.all() 
    print(articles)
    print("Hello")
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'articles': articles,
    }
    return render(request, 'arcada/index.html', context=data)

def about(request):
    data = {
        'title': 'О сайте',
        'menu': menu,
    }
    return render(request, 'arcada/about.html', context=data)

def article_detail(request, article_slug):
    article = get_object_or_404(GameArticle.published.all(), slug=article_slug)
    return render(request, 'arcada/article_detail.html', {'article': article})

def page_not_found(request, exception):
    from django.http import HttpResponseNotFound
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")