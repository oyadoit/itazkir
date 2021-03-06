# Generated by Django 3.0.3 on 2020-02-21 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reminder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('data', models.TextField()),
                ('reminder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reminder.Reminder')),
            ],
        ),
    ]
