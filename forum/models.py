from django.db import models
from django.utils import timezone
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from login.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(to='forum.Post', to_field='id', on_delete=models.CASCADE, related_name='comments')
    # content = models.TextField()
    # content = RichTextField()  # 富文本编辑器
    content = RichTextUploadingField(max_length=204800)  # 富文本编辑器
    created = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='replyers')
    reply_to_comment = models.ForeignKey(to='Comment', to_field='id', null=True, blank=True, on_delete=models.CASCADE,
                                         related_name='replyToComment')
    absoluteUps = models.IntegerField(default=0)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.content[:20]


class Zone(models.Model):
    title = models.CharField(max_length=64)  # 空间名称
    theme = models.CharField(max_length=64)


# 帖子表
class Post(models.Model):
    sections = (
        (1, "讨论区"),
        (2, "刷题区"),
        (3, "校园区"),
        (4, "课程推荐区"),
        (5, "资源区"),
    )
    # section = models.CharField(verbose_name='板块', max_length=32, choices=sections, default="讨论区")
    section = models.CharField(verbose_name='板块', max_length=32, choices=sections, default="讨论区")
    level_restriction = models.IntegerField(verbose_name="等级限制", default=0)
    create_time = models.DateField(verbose_name='创建时间', default=timezone.now)
    last_edit = models.DateTimeField(verbose_name='最后一次更新时间', auto_now=True, auto_now_add=False)
    # photo = models.ImageField(verbose_name='图片', upload_to='img', null=True)
    content = RichTextUploadingField(max_length=204800)
    title = models.CharField(verbose_name='帖子标题', max_length=64)
    author = models.ForeignKey(to='login.User', to_field='id', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    is_top = models.BooleanField(default=False)
    comment_count = models.IntegerField(default=0)
    absoluteUps = models.IntegerField(default=0)

    class Meta:
        ordering = ('-create_time',)

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_absolute_url(self):
        # print(str(self.id))
        return reverse('PostContent', kwargs={"s": str(self.id)})


# class Comment(models.Model):
#     user = models.ForeignKey(to='login.User', to_field='id', on_delete=models.CASCADE)
#     post = models.ForeignKey(to='Post', to_field='id', on_delete=models.CASCADE)
#     content = models.CharField(max_length=255)
#     create_time = models.DateTimeField(auto_now_add=True)
#     parent = models.ForeignKey(to='self', to_field='id', null=True, blank=True, on_delete=models.CASCADE)

# 点赞点踩
class UpAndDown(models.Model):
    user = models.ForeignKey(to='login.User', to_field='id', on_delete=models.CASCADE)
    post = models.ForeignKey(to='Post', to_field='id', on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(to='Comment', to_field='id', on_delete=models.CASCADE, null=True)

# 提及
# class Mention(models.Model):
#     id = models.AutoField(primary_key=True)
#     src_user_id = models.ForeignKey(to='login.User', to_field='id', on_delete=models.CASCADE)
#     tar_user_id = models.ForeignKey(to='login.User', to_field='id', on_delete=models.CASCADE)
#     post_id = models.ForeignKey(to='forum.Post', to_field='id', on_delete=models.CASCADE)
#     comment_id = models.ForeignKey(to='forum.Comment', to_field='id', on_delete=models.CASCADE)


