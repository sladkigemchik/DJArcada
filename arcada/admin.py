from django.contrib import admin, messages
from .models import GameArticle, Category, TagPost, UserProfile


class PriceFilter(admin.SimpleListFilter):
    title = 'Цена'
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return [
            ('free', 'Бесплатные (0 руб.)'),
            ('paid', 'Платные (> 0 руб.)'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'free':
            return queryset.filter(price=0)
        if self.value() == 'paid':
            return queryset.filter(price__gt=0)
        return queryset


@admin.register(GameArticle)
class GameArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'game_name', 'price', 'status', 'cat', 'time_create', 'brief_info')
    list_display_links = ('title',)
    list_editable = ('status', 'price')
    ordering = ['-time_create']
    list_per_page = 10
    search_fields = ['title', 'game_name']
    list_filter = ['cat', 'status', 'time_create', PriceFilter]
    fields = ['title', 'slug', 'game_name', 'genre', 'price', 'content', 'cat', 'tags', 'status']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    actions = ['make_published', 'make_draft']

    @admin.display(description="Краткое описание")
    def brief_info(self, obj):
        return f"Текст: {len(obj.content)} симв."

    @admin.action(description="Опубликовать выбранные записи")
    def make_published(self, request, queryset):
        count = queryset.update(status=GameArticle.Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} записей.")

    @admin.action(description="Снять с публикации")
    def make_draft(self, request, queryset):
        count = queryset.update(status=GameArticle.Status.DRAFT)
        self.message_user(request, f"Снято с публикации {count} записей.", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug')
    search_fields = ('tag',)
    prepopulated_fields = {'slug': ('tag',)}


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bio', 'phone')

admin.site.site_header = "Панель управления Arcada Project"
admin.site.site_title = "Arcada Admin"
admin.site.index_title = "Добро пожаловать в панель администратора"