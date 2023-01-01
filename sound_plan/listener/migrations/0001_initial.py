# Generated by Django 4.1.4 on 2022-12-31 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlist_name', models.CharField(max_length=50)),
                ('songs', models.ManyToManyField(to='player.song')),
            ],
        ),
        migrations.CreateModel(
            name='Listener',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=264)),
                ('last_name', models.CharField(max_length=264)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='listener.playlist')),
            ],
        ),
    ]