from django.shortcuts import redirect, render, get_object_or_404
from arcada.models import GameArticle, Category, TagPost
from .forms import AddGameForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

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

@login_required
def add_game(request):
    if request.method == 'POST':
        form = AddGameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save(commit=False)
            game.author = request.user   
            game.save()
            form.save_m2m()  
            return redirect('home')
    else:
        form = AddGameForm()
    return render(request, 'arcada/add_game.html', {'form': form, 'title': 'Добавить игру'})


@csrf_exempt
@require_http_methods(["POST"])
def ask_yandex_gpt(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('question', '')

        if not user_message:
            return JsonResponse({'error': 'Пустой запрос'}, status=400)

        YANDEX_FOLDER_ID = 'b1gask1fg9a7nmj0g2gt'
        YANDEX_API_KEY = 'AQVNw81AyPZPAEOPsOfwBLaQXK_gl3VMO1XnqOD9'
        YANDEX_MODEL = "aliceai-llm"  

        client = openai.OpenAI(
            api_key=YANDEX_API_KEY,
            project=YANDEX_FOLDER_ID,
            base_url="https://ai.api.cloud.yandex.net/v1"
        )

        response = client.responses.create(
            model=f"gpt://{YANDEX_FOLDER_ID}/{YANDEX_MODEL}",
            input=user_message,
            temperature=0.8,
            max_output_tokens=1000
        )

        answer = response.output[0].content[0].text

        return JsonResponse({'answer': answer})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def ai_chat(request):
    return render(request, 'arcada/ai_chat.html', {'title': 'Чат с ИИ'})