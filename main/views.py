from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives  # класс для создание объекта письма с html
from django.template.loader import render_to_string  # функция, которая рендерит наш html в текст
from django.shortcuts import get_object_or_404, redirect

from .models import Post, Reply
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    model = Post
    ordering = '-date_add'
    template_name = 'post_list.html'
    context_object_name = 'post'
    paginate_by = 10


class UserPostList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-date_add'
    template_name = 'user_post_list.html'
    context_object_name = 'post'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'



# def send_post_notification(post, subscribers):
#     """ Рассылка на почту """
#     for user in subscribers:
#         # Получаем наш html с учетом пользователя
#         html_content = render_to_string(
#             'email_post_created.html',
#             {
#                 'post': post,
#                 'user': user,
#             }
#         )
#
#         # Отправка письма
#         msg = EmailMultiAlternatives(
#             subject=f'{post.title} | {post.date_add.strftime("%Y-%m-%d")}',
#             body=post.text,
#             from_email='django.emailsender@yandex.ru',
#             to=[user.email],
#         )
#         msg.attach_alternative(html_content, "text/html")  # добавляем html
#         print(f'DEBUG: Sended email - {user.email}')
#         msg.send()  # отсылаем


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()

        # Сохраняем категории через промежуточную модель PostCategory
        # categories = form.cleaned_data['category']
        # for category in categories:
        #     PostCategory.objects.create(post=post, category=category)

        # Отправка уведомлений
        # Собираем все email подписчиков
        # subscribers = set()
        # for category in post.category.all():
        #     for user in category.subscribers.all():
        #         subscribers.add(user)

        # Отправка писем каждому подписчику
        # send_post_notification(post, subscribers)

        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('post.change_post')

    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('post.delete_post')

    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')




















