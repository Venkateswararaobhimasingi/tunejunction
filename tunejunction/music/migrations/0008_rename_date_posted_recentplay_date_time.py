# Generated by Django 4.2.3 on 2024-04-12 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_recentplay'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recentplay',
            old_name='date_posted',
            new_name='date_time',
        ),
    ]
