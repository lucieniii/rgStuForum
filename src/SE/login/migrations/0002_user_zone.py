# Generated by Django 2.2.12 on 2020-05-29 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='zone',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.Zone'),
        ),
    ]