import random
import string

from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.contrib.auth import login, get_backends, logout

from .forms import SignUpForm, ConfirmationForm
from .models import EmailConfirmation


def generate_confirmation_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # пользователь не активен, пока не подтвердит email
            user.save()

            confirmation_code = generate_confirmation_code()
            expiration_time = timezone.now() + timezone.timedelta(hours=1)
            EmailConfirmation.objects.create(user=user, confirmation_code=confirmation_code, expiration_time=expiration_time)

            html_content = render_to_string(
                'sign/email_confirmation_signup_message.html',
                {
                    'confirmation_code': confirmation_code,
                    'user': user,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'Your confirmation code | MMOhub',
                body='Your confirmation code is..',
                from_email='django.emailsender@yandex.ru',
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            print(f'DEBUG: Sended email - {user.email}')
            msg.send()

            return redirect('confirm_email')
    else:
        form = SignUpForm()
    return render(request, 'sign/signup.html', {'form': form})


def confirm_email_view(request):
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['confirmation_code']
            try:
                confirmation = EmailConfirmation.objects.get(confirmation_code=code)
                if confirmation.is_valid():
                    user = confirmation.user
                    user.is_active = True
                    user.save()
                    confirmation.delete()

                    backend = get_backends()[0]  # Определяю бекенд аунтификации
                    user.backend = f'{backend.__module__}.{backend.__class__.__name__}'

                    login(request, user)
                    return redirect('post_list')
                else:
                    form.add_error(None, 'Срок действия кода подтверждения истек')
            except EmailConfirmation.DoesNotExist:
                form.add_error(None, 'Неверный код подтверждения')
    else:
        form = ConfirmationForm()
    return render(request, 'sign/confirmation_email.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'sign/logout.html')
