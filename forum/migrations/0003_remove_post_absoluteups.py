# Generated by Django 2.2.12 on 2020-06-12 00:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_comment_absoluteups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='absoluteUps',
        ),
    ]
