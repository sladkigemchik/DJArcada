from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import GameArticle, Category, TagPost
from .forms import AddGameForm
from django.db.models import Q

# Проверки прав доступа
def can_moderate(user):
    return user.is_authenticated and user.role in ['moderator', 'admin']

def home(request):
    """Главная - только опубликованные статьи"""
    articles = GameArticle.objects.filter(status=1).order_by('-time_create')
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'arcada/index.html', {'page_obj': page_obj})

def about(request):
    return render(request, 'arcada/about.html')

def article_detail(request, article_slug):
    article = get_object_or_404(GameArticle, slug=article_slug)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'delete' and request.user.role in ['moderator', 'admin']:
            article.delete()
            messages.success(request, 'Статья удалена!')
            return redirect('home')
        
        elif action == 'approve' and request.user.role in ['moderator', 'admin']:
            article.status = 1
            article.save()
            messages.success(request, 'Статья опубликована!')
            return redirect('home')
    
    if article.status != 1 and request.user.role not in ['moderator', 'admin']:
        raise Http404("Статья не найдена")
    
    return render(request, 'arcada/article_detail.html', {'article': article})

def category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    articles = GameArticle.objects.filter(cat=category, status=1)
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'arcada/category.html', {
        'category': category,
        'page_obj': page_obj,
    })

import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt
@require_http_methods(["POST"])
def ask_yandex_gpt(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('question', '')

        if not user_message:
            return JsonResponse({'error': 'Пустой запрос'}, status=400)

        YANDEX_FOLDER_ID = ''
        YANDEX_API_KEY = ''
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

def tag(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    articles = GameArticle.objects.filter(tags=tag, status=1)
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'arcada/tag.html', {
        'tag': tag,
        'page_obj': page_obj,
    })

@login_required
def add_game(request):
    """Любой авторизованный может добавить статью"""
    if request.method == 'POST':
        form = AddGameForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            
            if request.user.role in ['moderator', 'admin']:
                article.status = 1  # Опубликовано
                messages.success(request, 'Статья опубликована!')
            else:
                article.status = 2  # На модерации
                messages.success(request, 'Статья отправлена на модерацию!')
            
            article.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = AddGameForm()
    
    return render(request, 'arcada/add_game.html', {'form': form})

@login_required
@user_passes_test(can_moderate)
def pending_articles(request):
    """Статьи на модерации - только для модераторов"""
    articles = GameArticle.objects.filter(status=2).order_by('-time_create')
    return render(request, 'arcada/pending_articles.html', {'articles': articles})

@login_required
@user_passes_test(can_moderate)
def approve_article(request, article_id):
    article = get_object_or_404(GameArticle, id=article_id)
    article.status = 1
    article.save()
    messages.success(request, f'Статья "{article.title}" опубликована!')
    return redirect('home')  # НА ГЛАВНУЮ

@login_required
@user_passes_test(can_moderate)
def reject_article(request, article_id):
    """Отклонить статью"""
    article = get_object_or_404(GameArticle, id=article_id)
    article.status = 0  # Черновик
    article.save()
    messages.warning(request, f'Статья "{article.title}" отклонена')
    return redirect('home')

def search(request):
    query = request.GET.get('q', '')
    if query:
        articles = GameArticle.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(game_name__icontains=query),
            status=1
        ).distinct()
    else:
        articles = GameArticle.objects.none()
    
    return render(request, 'arcada/search.html', {
        'articles': articles,
        'query': query,
    })


def ai_chat(request):
    return render(request, 'arcada/ai_chat.html')

@login_required
@user_passes_test(lambda u: u.role in ['moderator', 'admin'])
def edit_article(request, article_id):
    """Редактирование статьи - только для модераторов и админов"""
    article = get_object_or_404(GameArticle, id=article_id)
    
    if request.method == 'POST':
        form = AddGameForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            form.save_m2m()
            
            # Проверяем, какая кнопка была нажата
            if request.POST.get('action') == 'publish':
                article.status = 1  # Опубликовано
                article.save()
                messages.success(request, 'Статья опубликована!')
            else:
                messages.success(request, 'Статья сохранена как черновик!')
            
            return redirect('article_detail', article_slug=article.slug)
    else:
        form = AddGameForm(instance=article)
    
    return render(request, 'arcada/edit_article.html', {
        'form': form,
        'article': article,
    })

@login_required
@user_passes_test(lambda u: u.role in ['moderator', 'admin'])
def delete_article(request, article_id):
    article = get_object_or_404(GameArticle, id=article_id)
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Статья удалена!')
        return redirect('home')  # НА ГЛАВНУЮ