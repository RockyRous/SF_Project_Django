from django.contrib import admin
from .models import Post, Reply, Newsletter

admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(Newsletter)
