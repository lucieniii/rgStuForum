# Generated by Django 2.2.5 on 2020-06-11 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(blank=True, null=True, verbose_name='年龄'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='user_avatar/', verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='user',
            name='c_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='注册时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='user',
            name='exp',
            field=models.IntegerField(default=0, verbose_name='经验值'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='管理员'),
        ),
        migrations.AlterField(
            model_name='user',
            name='major',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='专业'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=128, unique=True, verbose_name='用户名'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=256, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='user',
            name='school',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='学校'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('male', '男'), ('female', '女')], default='男', max_length=32, verbose_name='性别'),
        ),
    ]
