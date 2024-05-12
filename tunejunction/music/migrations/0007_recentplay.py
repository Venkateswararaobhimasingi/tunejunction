# Generated by Django 4.2.3 on 2024-04-12 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0006_audiodetail_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recentplay',
            fields=[
                ('recent_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('audio_id', models.CharField(default='', max_length=10000000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]