from django.contrib import admin
from .models import AudioDetail,Listenlater,Recentplay,Trend
# Register your models here.
admin.site.register(AudioDetail)
admin.site.register(Listenlater)
admin.site.register(Recentplay)
admin.site.register(Trend)