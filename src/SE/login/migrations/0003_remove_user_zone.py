# Generated by Django 2.2.5 on 2020-06-03 00:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_user_zone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='zone',
        ),
    ]
