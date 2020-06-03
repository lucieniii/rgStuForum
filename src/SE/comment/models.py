from django.db import models
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
