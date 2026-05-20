from django import forms
from .models import GameArticle, Category, TagPost


class AddGameForm(forms.ModelForm):
    class Meta:
        model = GameArticle
        fields = ['title', 'slug', 'game_name', 'genre', 'price', 'content', 'cat', 'tags', 'status', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'game_name': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Категория",
        empty_label="Категория не выбрана",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=TagPost.objects.all(),
        label="Теги",
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    status = forms.BooleanField(
        required=False,
        label="Опубликовать",
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )

    def clean_status(self):
        value = self.cleaned_data.get('status')
        if value is True:
            return GameArticle.Status.PUBLISHED  
        return GameArticle.Status.DRAFT  