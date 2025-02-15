from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from django.utils import timezone

from allauth.account.forms import SignupForm


class EmailConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=6)
    expiration_time = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.expiration_time


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")

    class Meta:
        model = User
        fields = ("username",
                  # "first_name",
                  # "last_name",
                  "email",
                  "password1",
                  "password2", )


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
