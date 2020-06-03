from django.contrib import admin
from .models import Post, Tag, Comment

# 注册ArticlePost到admin中
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
# Register your models here.
