from django.urls import path
from .views import *

urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view()),
   path('create_post/', PostCreate.as_view(), name='post_edit'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='Post_delete'),
]
