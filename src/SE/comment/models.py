from django.db import models


class Comment(models.Model):
    user = models.ForeignKey(to='login.User', to_field='id', on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(to='forum.Post', to_field='id', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.content[:20]
