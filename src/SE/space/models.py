from django.db import models


# Create your models here.
class UserSpace(models.Model):
    UserID = models.ForeignKey(primary_key=True, to='User', to_field='id', null=False, on_delete=models.CASCADE)
    Introduction = models.CharField(verbose_name='空间简介', max_length=100)
    BGImagePath = models.ImageField(verbose_name='背景图')


class FavoritePost(models.Model):
    UserID = models.ForeignKey(primary_key=True, to='User', to_field='id', null=False, on_delete=models.CASCADE)
    PostID = models.ForeignKey(primary_key=True, to='Post', to_field='id', null=False, on_delete=models.CASCADE)
    FavoriteTime = models.DateTimeField(verbose_name='收藏时间', auto_now=True, auto_now_add=True)


class Follow(models.Model):
    FollowerID = models.ForeignKey(primary_key=True, to='User', to_field='id', null=False, on_delete=models.CASCADE)
    FollowedID = models.ForeignKey(primary_key=True, to='User', to_field='id', null=False, on_delete=models.CASCADE)
    FollowTime = models.DateTimeField(verbose_name='关注时间', auto_now=False, auto_now_add=True)


class Message(models.Model):
    SenderID = models.ForeignKey(primary_key=True, to='User', to_field='id', null=False, on_delete=models.CASCADE)
    ReceiverID = models.ForeignKey(primary_key=True, to='User', to_field='id', null=False, on_delete=models.CASCADE)
    SendTime = models.DateTimeField(verbose_name='发送时间', auto_now=False, auto_now_add=True)
    ReadFlag = models.BooleanField(verbose_name="是否已读", default=False)


class BlackList(models.Model):
    BlockerID = models.ForeignKey(primary_key=True, to='User', to_field='id', null=False, on_delete=models.CASCADE)
    BlockedID = models.ForeignKey(primary_key=True, to='User', to_field='id', null=False, on_delete=models.CASCADE)
    BlockTime = models.DateTimeField(verbose_name='拉黑时间', auto_now=True, auto_now_add=True)


class Permission(models.Model):
    UserID = models.ForeignKey(primary_key=True, to='User', to_field='id', null=False, on_delete=models.CASCADE)
    ViewPostPermission = models.BooleanField(verbose_name="查看发帖权限", default=True)
    ViewCommentPermission = models.BooleanField(verbose_name="查看回复权限", default=True)
    ViewFollowPermission = models.BooleanField(verbose_name="查看关注用户权限", default=True)
    ViewFavoritePermission = models.BooleanField(verbose_name="查看收藏帖子权限", default=True)
    ViewSelfInfoPermission = models.BooleanField(verbose_name="查看个人信息权限", default=True)
