from django.db import models
from django.utils import timezone
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from login.models import User


class Comment(MPTTModel):
    user = models.ForeignKey(to='login.User', to_field='id', on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(to='forum.Post', to_field='id', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # 新增，记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    # 替换 Meta 为 MPTTMeta
    # class Meta:
    #     ordering = ('created',)
    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return self.content[:20]


class Zone(models.Model):
    title = models.CharField(max_length=64)  # 空间名称
    theme = models.CharField(max_length=64)


# 帖子表
class Post(models.Model):
    tag = models.ForeignKey(to='Tag', to_field='id', null=True, on_delete=models.CASCADE)
    create_time = models.DateField(verbose_name='创建时间', default=timezone.now)
    last_edit = models.DateTimeField(verbose_name='最后一次更新时间', auto_now=True, auto_now_add=False)
    # photo = models.ImageField(verbose_name='图片', upload_to='img', null=True)
    content = models.TextField()
    title = models.CharField(verbose_name='帖子标题', max_length=64)
    author = models.ForeignKey(to='login.User', to_field='id', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    is_top = models.BooleanField(default=False)

    class Meta:
        ordering = ('-create_time',)

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_absolute_url(self):
        return reverse('post:post_detail', args=[self.id])


# class Comment(models.Model):
#     user = models.ForeignKey(to='login.User', to_field='id', on_delete=models.CASCADE)
#     post = models.ForeignKey(to='Post', to_field='id', on_delete=models.CASCADE)
#     content = models.CharField(max_length=255)
#     create_time = models.DateTimeField(auto_now_add=True)
#     parent = models.ForeignKey(to='self', to_field='id', null=True, blank=True, on_delete=models.CASCADE)


# 分类表
class Tag(models.Model):
    name = models.CharField(verbose_name='分类名称', max_length=16)


# 点赞点踩
class UpAndDown(models.Model):
    user = models.ForeignKey(to='login.User', to_field='id', on_delete=models.CASCADE)
    post = models.ForeignKey(to='Post', to_field='id', on_delete=models.CASCADE)
    is_up = models.BooleanField()  # True表示点赞，False表示点踩

    class Meta:
        unique_together = (('user', 'post'),)  # 用户只能点赞或点踩

# 提及
# class Mention(models.Model):
#     id = models.AutoField(primary_key=True)
#     src_user_id = models.ForeignKey(to='login.User', to_field='id', on_delete=models.CASCADE)
#     tar_user_id = models.ForeignKey(to='login.User', to_field='id', on_delete=models.CASCADE)
#     post_id = models.ForeignKey(to='forum.Post', to_field='id', on_delete=models.CASCADE)
#     comment_id = models.ForeignKey(to='forum.Comment', to_field='id', on_delete=models.CASCADE)
