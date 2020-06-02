from django.contrib import admin
from .models import Post, Tag

# 注册ArticlePost到admin中
admin.site.register(Post)
admin.site.register(Tag)
# Register your models here.
