# Generated by Django 4.1.4 on 2023-01-01 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listener', '0003_remove_listener_playlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='listener',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='listener.listener'),
        ),
    ]
