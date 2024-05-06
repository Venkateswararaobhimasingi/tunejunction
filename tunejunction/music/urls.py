from django.urls import path
from .views import (PostListView,ListenLaterListView,RecentListView,YourCountListView,TopTrend)
from . import views
urlpatterns = [
   
    path('upload/',views.upload,name='upload'),
    path('', PostListView.as_view(),name='home'),
    
    path('play/<int:id>/',views.play,name='play'),
   
    path('play/<int:id>/playnext/',views.playnext,name='playnext'),
    
    path('play/<int:id>/playpast/',views.playpast,name='playpast'),

    path('listenlater/listenplay/<int:id>/',views.listenplay,name='listenplay'),
    path('listenlater/',ListenLaterListView.as_view(),name='listenlater'),
    path('listenlateradd/',views.listenlateradd,name='listenlateradd'),
    path('listenlater/listenplay/<int:id>/listenplaynext/',views.listenplaynext,name='listenplaynext'),
    
    path('listenlater/listenplay/<int:id>/listenplaypast/',views.listenplaypast,name='listenplaypast'),
    path('listenlater/<int:id>/delete/', views.delete_audio, name='delete_audio'),

    path('recentplay/<int:id>/',views.recentplay,name='recentplay'),
    path('trendcount/<int:id>/',views.trend,name='trendcount'),
    path('recent/',RecentListView.as_view(),name='recent'),

    path('recent/play/<int:id>/',views.recent_play,name='recentplay1'),

    path('yourcount/',YourCountListView.as_view(),name='yourcount'),
    path('yourcount/play/<int:id>/',views.yourcount_play,name='yourcount1'),

    path('trend/',TopTrend.as_view(),name='trend'),
    path('trend/play/<int:id>/',views.trendplay1,name='trendplay1'),
    
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('design/',views.design,name='design'),
    path('search/',views.search,name='search'),

    
    

]