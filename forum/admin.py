from django.contrib import admin
from .models import Post, Comment, UpAndDown

# 注册ArticlePost到admin中
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UpAndDown)
# Register your models here.
