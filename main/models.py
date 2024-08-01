from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """ Обьявления """
    # При создании автор должен автоматически выставляться на пользователя. Полагаю это делается во вьёшке.

    heal = 'heal'
    category_list = [
        (heal, 'Хил'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()  # todo: format text+img+video+etc
    category = models.CharField(max_length=255, choices=category_list, default=heal)
    date_add = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # def preview(self):
    #     short_text = self.text[:124] + '...'
    #     return short_text
    #
    def __str__(self):
        return f'({self.id}) {self.title}'


class Reply(models.Model):
    """ Отклики """
    title = models.CharField(max_length=255)
    content = models.TextField()  # todo: format text+img+video+etc

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'({self.ad.title}) {self.title}'


