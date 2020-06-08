from django.contrib import admin
from .models import Post, Section, Comment

# 注册ArticlePost到admin中
admin.site.register(Post)
admin.site.register(Section)
admin.site.register(Comment)
# Register your models here.
