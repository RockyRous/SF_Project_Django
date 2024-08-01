from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    # category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Post
        fields = [
            # 'author',
            'title',
            'content',
            'category',
        ]
        labels = {
            # 'author': 'Автор',
            'title': 'Заголовок',
            'content': 'Содержание',
            'category': 'Категория'
        }

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("content")
        name = cleaned_data.get("title")
        # if name == description:
        #     raise ValidationError(
        #         "Текст не должен быть идентичным названию."
        #     )
        # if description is not None and len(description) < 20:
        #     raise ValidationError({
        #         "description": "Текст не может быть менее 20 символов."
        #     })
        return cleaned_data






