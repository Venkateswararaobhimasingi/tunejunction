from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

# Create your models here.
class AudioDetail(models.Model):
    id=models.AutoField(primary_key=True)
    audio_file = models.FileField(upload_to='audio_files/')
    title = models.CharField(max_length=100, blank=True)
    artist = models.CharField(max_length=100, blank=True)
    album = models.CharField(max_length=100, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    image = models.ImageField(default='default1.jpg',upload_to='audio_images/', blank=True, null=True)
    duration = models.FloatField(default=0.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None,null=True)

    def save(self,*args,**kawrgs):
        super().save(*args,**kawrgs)

        img=Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)



    

    

    def __str__(self):
        return self.title

class Listenlater(models.Model):
    listen_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_id = models.CharField(max_length=10000000, default="")   


class Recentplay(models.Model):
    recent_id= models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=timezone.now)
    audio_id = models.CharField(max_length=10000000, default="")  


class Trend(models.Model):
    trend_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_id = models.CharField(max_length=10000000, default="")
    count_of_song= models.IntegerField(default=1)