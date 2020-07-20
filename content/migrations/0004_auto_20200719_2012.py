# Generated by Django 3.0.7 on 2020-07-19 20:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20200708_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='content',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
