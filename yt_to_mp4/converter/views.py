from django.shortcuts import render
from django.http import HttpResponse
from pytube import YouTube
from .forms import YouTubeURLForm

def home(request):
    if request.method == 'POST':
        form = YouTubeURLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            yt = YouTube(url)
            stream = yt.streams.filter(file_extension='mp4', res="720p").first()
            video_title = yt.title + ".mp4"
            video_path = stream.download()  # Download the video to a temporary location

            with open(video_path, 'rb') as video_file:
                response = HttpResponse(video_file.read(), content_type='video/mp4')
                response['Content-Disposition'] = f'attachment; filename="{video_title}"'
                return response
    else:
        form = YouTubeURLForm()

    return render(request, 'converter/home.html', {'form': form})
