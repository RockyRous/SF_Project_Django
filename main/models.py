from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Post(models.Model):
    """ Обьявления """
    tank = 'Танк'
    heal = 'Хил'
    dd = 'ДД'
    merchants = 'Торговцы'
    guildmasters = 'Гильдмастеры'
    questgivers = 'Квестгиверы'
    blacksmiths = 'Кузнецы'
    tanners = 'Кожевники'
    potion_makers = 'Зельевары'
    spell_masters = 'Мастера Заклинаний'
    category_list = [
        (tank, 'Танк'),
        (heal, 'Хил'),
        (dd, 'ДД'),
        (merchants, 'Торговцы'),
        (guildmasters, 'Гильдмастеры'),
        (questgivers, 'Квестгиверы'),
        (blacksmiths, 'Кузнецы'),
        (tanners, 'Кожевники'),
        (potion_makers, 'Зельевары'),
        (spell_masters, 'Мастера Заклинаний'),
    ]

    title = models.CharField(max_length=255)
    content = RichTextField()
    category = models.CharField(max_length=255, choices=category_list, default=heal)
    date_add = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'({self.id}) {self.title}'


class Reply(models.Model):
    """ Отклики """
    title = models.CharField(max_length=255)
    content = RichTextField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'({self.ad.title}) {self.title}'


class Newsletter(models.Model):
    """ Модель для новостной рассылки """
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
