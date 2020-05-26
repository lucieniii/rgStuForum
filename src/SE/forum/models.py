from django.db import models


class Zone(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)  # 空间名称
    theme = models.CharField(max_length=64)


# 帖子表
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.ForeignKey(to='Tag', to_field='id', null=False, on_delete=models.CASCADE)
    create_time = models.DateField(verbose_name='创建时间', auto_now=False, auto_now_add=True)
    last_edit = models.DateTimeField(verbose_name='最后一次更新时间', auto_now=True, auto_now_add=False)
    photo = models.ImageField(verbose_name='图片')
    content = models.CharField(verbose_name='帖子正文', max_length=3000)
    title = models.CharField(verbose_name='帖子标题', max_length=64)
    user = models.ForeignKey(to='login.User', to_field='id', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    is_changed = models.BooleanField(verbose_name="是否已更新", default=False)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='login.User', to_field='id', on_delete=models.CASCADE)
    post = models.ForeignKey(to='Post', to_field='id', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(to='self', to_field='id', null=True, blank=True, on_delete=models.CASCADE)


# 分类表
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='分类名称', max_length=16)


# 点赞点踩
class UpAndDown(models.Model):
    id = models.AutoField(primary_key=True)
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
