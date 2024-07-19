from django.shortcuts import render
from django.http import FileResponse
from .forms import VideoSettingsForm
from .models import Video
from urllib.parse import quote
from .services.video_generator import generate_video
import os

def index(request):
    if request.method == 'POST':
        form = VideoSettingsForm(request.POST)
        if form.is_valid():
            video_instance = form.save()
            settings = {
                'title': video_instance.title,
                'text': video_instance.text,
                'duration': video_instance.duration,
                'resolution': video_instance.resolution,
                'background_color': video_instance.background_color,
                'font_color': video_instance.font_color,
                'font_scale': video_instance.font_scale,
                'thickness': video_instance.thickness,
                'include_stripe': video_instance.include_stripe,
                'stripe_color': video_instance.stripe_color,
                'output_path': f'media/{video_instance.title}.mp4'
            }
            video_stream = generate_video(settings)
            try:
                # Prepare file response
                filename = quote(f"{video_instance.title}.mp4")
                response = FileResponse(video_stream, content_type='video/mp4')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
            except FileNotFoundError:
                return render(request, 'error/error.html', {'error': 'File not found.'})
            except Exception as e:
                return render(request, 'error/error.html', {'error': str(e)})
    else:
        form = VideoSettingsForm()
    return render(request, 'video_creator/create_video.html', {'form': form})