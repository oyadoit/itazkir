# Generated by Django 3.0.3 on 2020-06-27 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
