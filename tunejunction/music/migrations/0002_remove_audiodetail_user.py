# Generated by Django 4.2.3 on 2024-03-29 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audiodetail',
            name='user',
        ),
    ]