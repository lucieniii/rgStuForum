# Generated by Django 2.2.12 on 2020-06-12 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '__first__'),
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('UserID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='login.User')),
                ('ViewPostPermission', models.BooleanField(default=True, verbose_name='查看发帖权限')),
                ('ViewCommentPermission', models.BooleanField(default=True, verbose_name='查看回复权限')),
                ('ViewFollowPermission', models.BooleanField(default=True, verbose_name='查看关注用户权限')),
                ('ViewFavoritePermission', models.BooleanField(default=True, verbose_name='查看收藏帖子权限')),
                ('ViewSelfInfoPermission', models.BooleanField(default=True, verbose_name='查看个人信息权限')),
            ],
        ),
        migrations.CreateModel(
            name='UserSpace',
            fields=[
                ('UserID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='login.User')),
                ('Introduction', models.CharField(max_length=100, verbose_name='空间简介')),
                ('BGImagePath', models.ImageField(upload_to='', verbose_name='背景图')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SendTime', models.DateTimeField(auto_now_add=True, verbose_name='发送时间')),
                ('ReadFlag', models.BooleanField(default=False, verbose_name='是否已读')),
                ('ReceiverID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiverID', to='login.User')),
                ('SenderID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='senderID', to='login.User')),
            ],
            options={
                'ordering': ['-SendTime'],
                'unique_together': {('SenderID', 'ReceiverID')},
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FollowTime', models.DateTimeField(auto_now_add=True, verbose_name='关注时间')),
                ('FollowedID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followedID', to='login.User')),
                ('FollowerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followerID', to='login.User')),
            ],
            options={
                'ordering': ['-FollowTime'],
                'unique_together': {('FollowerID', 'FollowedID')},
            },
        ),
        migrations.CreateModel(
            name='FavoritePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FavoriteTime', models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')),
                ('PostID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Post')),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.User')),
            ],
            options={
                'ordering': ['-FavoriteTime'],
                'unique_together': {('UserID', 'PostID')},
            },
        ),
        migrations.CreateModel(
            name='BlackList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BlockTime', models.DateTimeField(auto_now_add=True, verbose_name='拉黑时间')),
                ('BlockedID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blockedID', to='login.User')),
                ('BlockerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blockerID', to='login.User')),
            ],
            options={
                'ordering': ['-BlockTime'],
                'unique_together': {('BlockerID', 'BlockedID')},
            },
        ),
    ]
