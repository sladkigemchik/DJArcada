from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect
from django.urls import reverse

def index(request):
    return HttpResponse("Страница приложения arcada.")

def categories(request, game_id):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {game_id}</p>")

def categories_by_slug(request, game_slug):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {game_slug}</p>")

def archive(request, year):
    if year > "2024":
        raise Http404()
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

def old_archive(request):
    return redirect('archive', year=2020)

def reverse_example(request):
    url = reverse('game_id', args=(5,))
    return HttpResponse(f"URL через reverse: {url}")