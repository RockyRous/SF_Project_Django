from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from django.core.mail import send_mail

from .models import Post, Reply
from .forms import PostForm, ReplyForm, NewsletterForm

from MMOhub.config import sender_mail


def send_notification(post_author_email, post, reply_author_name):
    subject = f'Новый отклик на ваш пост: {post.title}'
    html_message = render_to_string('email/reply_notification.html', {
        'post': post,
        'reply_author_name': reply_author_name,
    })
    plain_message = strip_tags(html_message)
    from_email = sender_mail
    send_mail(subject, plain_message, from_email, [post_author_email], html_message=html_message)


class PostList(ListView):
    model = Post
    ordering = '-date_add'
    template_name = 'post_list.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.annotate(reply_count=Count('reply'))


class ReplyList(ListView):
    model = Reply
    template_name = 'reply_list.html'
    context_object_name = 'reply'

    def get_queryset(self):
        queryset = super().get_queryset()
        post_id = self.request.GET.get('post')
        if post_id:
            queryset = queryset.filter(ad_id=post_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.request.user)
        context['selected_post'] = self.request.GET.get('post')
        return context


class UserPostList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-date_add'
    template_name = 'post_list.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).annotate(reply_count=Count('reply'))


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = Reply.objects.filter(ad=self.object)
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class ReplyCreate(LoginRequiredMixin, CreateView):
    form_class = ReplyForm
    model = Reply
    template_name = 'post_detail.html'

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.author = self.request.user
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        reply.ad = post
        reply.save()

        send_notification(
            post_author_email=post.author.email,
            post=post,
            reply_author_name=self.request.user.username
        )

        return redirect('post_detail', pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class ReplyDelete(LoginRequiredMixin, DeleteView):
    model = Reply
    template_name = 'reply_delete.html'
    success_url = reverse_lazy('reply_list')


class ReplyAccept(View):
    def post(self, request, *args, **kwargs):
        reply = get_object_or_404(Reply, id=self.kwargs['pk'])

        self.send_acceptance_email(reply)

        return redirect('reply_list')

    def send_acceptance_email(self, reply):
        subject = f'Ваш отклик принят: {reply.title}'
        html_message = render_to_string('email/acceptance_notification.html', {
            'post_title': reply.ad.title,
            'reply_title': reply.title,
        })
        plain_message = strip_tags(html_message)
        from_email = sender_mail
        send_mail(subject, plain_message, from_email, [reply.author.email], html_message=html_message)


@staff_member_required
def create_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.sent_at = timezone.now()
            newsletter.save()

            users = User.objects.all()
            recipient_list = [user.email for user in users if user.email]

            send_mail(
                subject=newsletter.subject,
                message=newsletter.body,
                from_email=sender_mail,
                recipient_list=recipient_list,
            )

        return redirect('post_list')
    else:
        form = NewsletterForm()

    return render(request, 'create_newsletter.html', {'form': form})












