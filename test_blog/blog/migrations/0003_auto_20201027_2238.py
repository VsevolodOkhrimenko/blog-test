# Generated by Django 3.0.10 on 2020-10-27 22:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_auto_20201027_2200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='seen',
        ),
        migrations.AddField(
            model_name='post',
            name='seen',
            field=models.ManyToManyField(blank=True, related_name='seen_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]