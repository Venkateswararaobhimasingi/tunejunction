# Generated by Django 4.2.3 on 2024-04-07 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_listenlater'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiodetail',
            name='image',
            field=models.ImageField(blank=True, default='default1.jpg', null=True, upload_to='audio_images/'),
        ),
    ]
