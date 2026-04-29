from django.shortcuts import render, get_object_or_404
from arcada.models import GameArticle, Category, TagPost

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

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    articles = GameArticle.published.filter(cat=category)
    return render(request, 'arcada/index.html', {
        'title': category.name,
        'articles': articles,
        'menu': menu,
        'cat_selected': category.pk,
    })

def show_tag_articles(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    articles = tag.articles.filter(status=GameArticle.Status.PUBLISHED)
    return render(request, 'arcada/index.html', {
        'title': f'Тег: {tag.tag}',
        'articles': articles,
        'menu': menu,
        'cat_selected': None,
    })