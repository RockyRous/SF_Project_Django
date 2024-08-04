from django.urls import path
from django.contrib.auth.views import LoginView
from .views import signup_view, confirm_email_view, logout_view

urlpatterns = [
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),

    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('confirm_email/', confirm_email_view, name='confirm_email'),
]
