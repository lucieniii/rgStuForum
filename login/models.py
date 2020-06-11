from django.db import models
from django.urls import reverse

# Create your models here.


class User(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    # zone = models.OneToOneField(to='forum.Zone', to_field='id', null=True, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='user_avatar/', blank=True, null=True)
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]

    def get_absolute_url(self):
        return reverse('space', args=str(self.id))
