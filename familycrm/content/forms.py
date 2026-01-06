from django import forms
from .models import Content, Comment


class EditContentForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=0, max_value=5, label="Рейтинг")
    picture = forms.ImageField(required=False, widget=forms.FileInput)
    class Meta:
        model = Content
        fields = ('name', 'category', 'picture', 'rating', 'status')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message',]

class SearchForm(forms.Form):\
    search = forms.CharField(label="Поиск", max_length=100, required=True)