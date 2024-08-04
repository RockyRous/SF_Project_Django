from django import forms
from .models import Post, Reply


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'category',
        ]
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'category': 'Категория'
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = [
            'title',
            'content',
        ]
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
        }




