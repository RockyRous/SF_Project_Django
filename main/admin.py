from django.contrib import admin
from .models import Post, Reply
from ckeditor.widgets import CKEditorWidget


admin.site.register(Post)
admin.site.register(Reply)



