# Generated by Django 3.1 on 2021-03-17 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0014_auto_20210316_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes_unlikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='likes',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes_unlikes', to='main.post'),
        ),
    ]
