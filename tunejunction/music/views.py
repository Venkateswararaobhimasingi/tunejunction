from django.shortcuts import render, redirect,get_object_or_404
from .forms import AudioDetailForm
from django.utils import timezone
from django.http import JsonResponse
from .models import AudioDetail,Listenlater,Recentplay,Trend
import mutagen
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When
from django.shortcuts import redirect
from django.urls import reverse
import os
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.core.files import File
from PIL import Image, ImageTk
from collections import defaultdict
import io

def extract_audio_details(file_path):
    file_name = os.path.basename(file_path)
    audio_details = {}

    audio = mutagen.File(file_path)
    if audio:
        metadata = audio.tags
        audio_details['title'] = metadata.get("TIT2").text[0] if "TIT2" in metadata else "Unknown"
        audio_details['artist'] = ", ".join(metadata.get("TPE1").text) if "TPE1" in metadata else "Unknown"
        audio_details['album'] = metadata.get("TALB").text[0] if "TALB" in metadata else "Unknown"
        audio_details['genre'] = metadata.get("TCON").text[0] if "TCON" in metadata else "Unknown"
        audio_details['duration'] = round(((mutagen.File(file_path).info.length)/60),2)
        
        album_art = metadata.get("APIC:")
        if album_art:
            image_data = album_art.data
            image = Image.open(io.BytesIO(image_data))
            image_path = "media/audio_images/{}.jpg".format(file_name)  # Generate unique image file name
            image.save(image_path)
            audio_details['image'] = "audio_images/{}.jpg".format(file_name)
        else:
            audio_details['image'] = "default1.jpg"
        
        
    return audio_details

def upload(request):
    if request.method == 'POST':
        form = AudioDetailForm(request.POST, request.FILES)
        if form.is_valid():                                                                #HERE ONLY UPLOAD THE AUDIO THEN AUTOMATICALLY EXTRACT THE aLL DETAILS
            audio_detail = form.save(commit=False)
            audio_detail.title = request.FILES['audio_file'].name
            audio_detail.save()
            file_path = audio_detail.audio_file.path
            details = extract_audio_details(file_path)
            # Update the audio detail object with extracted details
            audio_detail.title = details.get('title')
            audio_detail.artist = details.get('artist')
            audio_detail.album = details.get('album')
            audio_detail.genre = details.get('genre')
            audio_detail.image = details.get('image')
            audio_detail.duration = details.get('duration')
            audio_detail.user=request.user
            audio_detail.save()
            
            return redirect('home')  # Redirect to a success page
    else:
        form = AudioDetailForm()
    return render(request, 'music/upload.html', {'form': form})

def home(request):
    audio_details = AudioDetail.objects.all()
    #song_ids = AudioDetail.objects.values_list('id', flat=True)
    #print(song_ids)
    #print(type(song_ids))
    #print(list(song_ids))
    return render(request, 'music/home.html', {'audio_details': audio_details})

class PostListView(ListView):
    model=AudioDetail
    template_name='music/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'audio_details'  #A way to refer to the object
    
    paginate_by=2
    def get_queryset(self):
        return AudioDetail.objects.all().order_by('-id')



class ListenLaterListView(ListView):
    model = AudioDetail
    template_name = 'music/listenlater.html'
    context_object_name = 'audio_details'
    paginate_by = 2

    def get_queryset(self):
        # Fetch audio ids from Listenlater model for current user
        wl = Listenlater.objects.filter(user=self.request.user)
        ids = [i.audio_id for i in wl]

        # Order AudioDetail queryset based on the order of ids in Listenlater
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
        queryset = AudioDetail.objects.filter(id__in=ids).order_by(preserved)

        # Reverse the queryset to display items from last to first
        queryset = queryset.reverse()

        return queryset
    


def play(request,id):
    
    audio_details=AudioDetail.objects.filter(id=id).first()
    print(audio_details)
    return render(request, 'music/play.html', {'audio_details': audio_details})


def playnext(request,id):
    song_ids = AudioDetail.objects.values_list('id', flat=True)
    song_ids=list(song_ids)
    
    if id==song_ids[-1] :
        id=song_ids[0]
        audio_details=AudioDetail.objects.filter(id=id).first()
        return redirect(reverse('play', kwargs={'id': id}))
    else:
        i=song_ids.index(id)
        id=song_ids[i+1]
        audio_details=AudioDetail.objects.filter(id=id).first()
        return redirect(reverse('play', kwargs={'id': id}))

def playpast(request,id):
    song_ids = AudioDetail.objects.values_list('id', flat=True)
    song_ids=list(song_ids)
    if id==song_ids[0] :
        id=song_ids[-1]
        audio_details=AudioDetail.objects.filter(id=id).first()
        return redirect(reverse('play', kwargs={'id': id}))
    else:
        i=song_ids.index(id)
        id=song_ids[i-1]
        audio_details=AudioDetail.objects.filter(id=id).first()
        return redirect(reverse('play', kwargs={'id': id}))


def listenlateradd(request):
    if request.method == "POST":
        user = request.user
        audio_id = request.POST['audio_id']

        watch = Listenlater.objects.filter(user=user)
        
        for i in watch:
            if audio_id == i.audio_id:
                message = "Your Video is Already Added"
                break
        else:
            listenlater = Listenlater(user=user, audio_id=audio_id)
            listenlater.save()
            message = "Your Video is Succesfully Added"

        audio_details = AudioDetail.objects.all()
       
        #return render(request, f"music/home.html", {'audio_details': audio_details, "message": message})
    

    return redirect('listenlater')


def listenplay(request,id):
    
    audio_details=AudioDetail.objects.filter(id=id).first()
    print(audio_details)
    return render(request, 'music/listenplay.html', {'audio_details': audio_details})

@login_required
def delete_audio(request, id):
    if request.method == 'POST':
        # Get the Listenlater object associated with the provided audio ID and the current user
        listenlater = get_object_or_404(Listenlater, audio_id=id, user=request.user)
        # Delete the object
        listenlater.delete()
        # Redirect to the listenlater page
        return redirect('listenlater')


@login_required
def listenplaynext(request, id):
    # Get the current user's playlist
    user = request.user
    song_ids = Listenlater.objects.filter(user=user).values_list('audio_id', flat=True)
    song_ids = list(song_ids)
    print(song_ids)

    if id == int(song_ids[-1]):
        id = int(song_ids[0])
        audio_details = AudioDetail.objects.filter(id=id).first()
        return redirect(reverse('listenplay', kwargs={'id': id}))
    else:
        i = song_ids.index(str(id))
        id = int(song_ids[i + 1])
        audio_details = AudioDetail.objects.filter(id=id).first()
        return redirect(reverse('listenplay', kwargs={'id': id}))

@login_required
def listenplaypast(request,id):
    user = request.user
    song_ids = Listenlater.objects.filter(user=user).values_list('audio_id', flat=True)
    song_ids = list(song_ids)
    print(song_ids)
    if id == int(song_ids[0]) :
        id=int(song_ids[-1])
        audio_details=AudioDetail.objects.filter(id=id).first()
        return redirect(reverse('listenplay', kwargs={'id': id}))
    else:
        i=song_ids.index(str(id))
        id=int(song_ids[i-1])
        audio_details=AudioDetail.objects.filter(id=id).first()
        return redirect(reverse('listenplay', kwargs={'id': id}))

def about(request):
    return render(request, 'music/about.html')

def contact(request):
    return render(request, 'music/contact.html')
def design(request):
    return render(request, 'music/design.html')


def recentplay(request,id):
    print('before'*50)

    if request.user.is_authenticated:

        audio_id=id
        print(audio_id)
        user=request.user
        recent_audio = Recentplay.objects.filter(user=user, audio_id=audio_id).first()

        if recent_audio:
           
            recent_audio.date_time = timezone.now()
            recent_audio.save()
            
        else:
            Recentplay.objects.create(user=user, audio_id=audio_id, date_time=timezone.now())
    return JsonResponse({'message': 'Audio ID received successfully'})
           

def trend(request,id):
    if request.user.is_authenticated:

        audio_id=id
        print(audio_id)
        user=request.user
        trend_entry = Trend.objects.filter(user=user, audio_id=audio_id).first()

        if trend_entry:
            trend_entry.count_of_song += 1
            trend_entry.save()
        else:
            # Create a new Trend entry
            Trend.objects.create(user=user, audio_id=audio_id, count_of_song=1)
    return JsonResponse({'message': 'trend Audio ID received successfully'})

'''def recent(request,id):
    if request.user.is_authenticated:
        wl = Recentplay.objects.filter(user=self.request.user)
        ids = [i.audio_id for i in wl]

        # Order AudioDetail queryset based on the order of ids in Listenlater
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
        audio_details = AudioDetail.objects.filter(id__in=ids).order_by(preserved)

    return render(request, 'music/recent.html', {'audio_details': audio_details})'''


class RecentListView(ListView):
    model = AudioDetail
    template_name = 'music/recent.html'
    context_object_name = 'audio_details'
    paginate_by = 10  # Number of items per page

    def get_queryset(self):
        if self.request.user.is_authenticated:
            wl = Recentplay.objects.filter(user=self.request.user).order_by('-date_time')[:20]
            ids = [i.audio_id for i in wl]
            print(ids)
        # Order AudioDetail queryset based on the order of ids in Listenlater
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
            queryset = AudioDetail.objects.filter(id__in=ids).order_by(preserved)
            recent=queryset
            return recent
        else:
            return Recentplay.objects.none()

class YourCountListView(ListView):
    model = AudioDetail
    template_name = 'music/yourcount.html'
    context_object_name = 'audio_details'
    paginate_by = 10  # Number of items per page

    def get_queryset(self):
        if self.request.user.is_authenticated:
            wl = Trend.objects.filter(user=self.request.user).order_by('-count_of_song')
            ids = [i.audio_id for i in wl]
            print(ids)
        # Order AudioDetail queryset based on the order of ids in Listenlater
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
            queryset = AudioDetail.objects.filter(id__in=ids).order_by(preserved)
            recent=queryset[0:10]
            return recent
        else:
            return Recentplay.objects.none()

def recent_play(request,id):
    audio_details=AudioDetail.objects.filter(id=id).first()
    return redirect(reverse('play', kwargs={'id': id}))

def yourcount_play(request,id):
    audio_details=AudioDetail.objects.filter(id=id).first()
    return redirect(reverse('play', kwargs={'id': id}))

def trendplay1(request,id):
    audio_details=AudioDetail.objects.filter(id=id).first()
    return redirect(reverse('play', kwargs={'id': id}))
class TopTrend(ListView):
    model = AudioDetail
    template_name = 'music/trend.html'
    context_object_name = 'audio_details'
    paginate_by = 10  # Number of items per page

    def get_queryset(self):
        if self.request.user.is_authenticated:
            wl = Trend.objects.all()
            ids = [i.audio_id for i in wl]
            related=[i.count_of_song for i in wl]
            print(ids)
            print(related)
            print('-'*20)
            id_related_sum = defaultdict(int)

# Iterate through the lists and calculate the sum of related values for each unique ID
            for id, value in zip(ids, related):
                id_related_sum[id] += value

# Get the unique IDs and their corresponding sums
            unique_ids = list(id_related_sum.keys())
            related_sums = list(id_related_sum.values())

# Sort the unique IDs based on the corresponding related sums in descending order
            sorted_ids = [id for _, id in sorted(zip(related_sums, unique_ids), reverse=True)]
            sorted_related_sums = sorted(related_sums, reverse=True)
            print(sorted_ids)
            print(sorted_related_sums)
        # Order AudioDetail queryset based on the order of ids in Listenlater
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(sorted_ids)])
            queryset = AudioDetail.objects.filter(id__in=ids).order_by(preserved)
            recent=queryset
            return recent
        else:
            return Recentplay.objects.none()


def search(request):
    query = request.GET.get('query')   
    
    # Filter AudioDetail objects based on the 'title' field
    audio_details = AudioDetail.objects.filter(title__icontains=query)  #filer whatyouwant__icontains=query
    
    return render(request, 'music/home.html', {'audio_details': audio_details})

def search(request):
    query = request.GET.get('query')   
    
    # Filter AudioDetail objects based on the 'title' field
    audio_details = AudioDetail.objects.filter(title__icontains=query)  #filer whatyouwant__icontains=query
    
    return render(request, 'music/home.html', {'audio_details': audio_details})