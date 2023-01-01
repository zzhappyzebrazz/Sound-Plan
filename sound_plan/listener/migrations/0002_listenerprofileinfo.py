# Generated by Django 4.1.4 on 2022-12-31 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listener', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListenerProfileInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portfolio', models.URLField(blank=True)),
                ('image', models.ImageField(default='player/listener/avatar_default.jpg', upload_to='player/listener/')),
                ('listener', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='listener.listener')),
            ],
        ),
    ]
