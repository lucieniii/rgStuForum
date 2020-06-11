# Generated by Django 2.2.12 on 2020-06-11 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='user_avatar/', verbose_name='头像')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='用户名')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='年龄')),
                ('password', models.CharField(max_length=256, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('sex', models.CharField(choices=[('male', '男'), ('female', '女')], default='男', max_length=32, verbose_name='性别')),
                ('school', models.CharField(blank=True, max_length=128, null=True, verbose_name='学校')),
                ('major', models.CharField(blank=True, max_length=128, null=True, verbose_name='专业')),
                ('is_admin', models.BooleanField(default=False, verbose_name='管理员')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('exp', models.IntegerField(default=0, verbose_name='经验值')),
            ],
            options={
                'ordering': ['-c_time'],
            },
        ),
    ]
