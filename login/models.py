import math

from django.db import models
from django.urls import reverse

# Create your models here.


class User(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    # zone = models.OneToOneField(to='forum.Zone', to_field='id', null=True, on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name='头像', upload_to='user_avatar/', blank=True, null=False, default='avatar.png')
    name = models.CharField(verbose_name='用户名', max_length=128, unique=True)
    age = models.IntegerField(verbose_name='年龄', blank=True, null=True)
    password = models.CharField(verbose_name='密码', max_length=256)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    sex = models.CharField(verbose_name='性别', max_length=32, choices=gender, default="男")
    school = models.CharField(verbose_name='学校', max_length=128, null=True, blank=True)
    major = models.CharField(verbose_name='专业', max_length=128, null=True, blank=True)
    is_admin = models.BooleanField(verbose_name='管理员', default=False)
    c_time = models.DateTimeField(verbose_name='注册时间', auto_now_add=True)
    exp = models.IntegerField(verbose_name='经验值', default=0)
    level = models.IntegerField(verbose_name='等级', default=1)
    is_ban = models.BooleanField(verbose_name='禁言', default=False)

    def save(self):
        if int(self.exp) < 0:
            self.exp = 0
        self.level = int(math.sqrt(int(self.exp)) // 10 + 1)
        super(User, self).save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]

    def get_absolute_url(self):
        return reverse('space', args=str(self.id))
