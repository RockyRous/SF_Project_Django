from django.urls import path
from .views import *

urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('my-posts/', UserPostList.as_view(), name='my_post_list'),
   path('reply/', ReplyList.as_view(), name='reply_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('<int:pk>/reply', ReplyCreate.as_view(), name='post_reply'),
   path('create_post/', PostCreate.as_view(), name='post_edit'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('<int:pk>/reply_delete/', ReplyDelete.as_view(), name='reply_delete'),
   path('<int:pk>/reply_accept/', ReplyAccept.as_view(), name='reply_accept'),
]
