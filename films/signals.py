from pathlib import Path
from django.db.models.signals import post_save
from django.dispatch import receiver
from moviepy.video.io.VideoFileClip import VideoFileClip
from .models import Film
from django.core.files import File
import os

BASE_DIR = Path(__file__).resolve().parent.parent


@receiver(post_save, sender=Film)
def create_gif_poster(sender, instance, created, **kwargs):

    if created:

        file_name = instance.video.path.split('/')[-1]
        dest_file_name_gif = file_name.split('.')[0] + '.gif'
        dest_file_name_poster = file_name.split('.')[0] + '.png'

        dest_path_gif = f'{BASE_DIR}/media/gifs/{dest_file_name_gif}'
        dest_path_poster = f'{BASE_DIR}/media/posters/{dest_file_name_poster}'
        poster = VideoFileClip(f'{BASE_DIR/instance.video.path}').save_frame(dest_path_poster, t=0.00)
        gif = VideoFileClip(f'{BASE_DIR/instance.video.path}').subclip(0, 2).write_gif(dest_path_gif)

        instance.gif.save(f'{dest_file_name_gif}', content=File(open(dest_path_gif, 'rb')))
        instance.poster.save(f'{dest_file_name_poster}', content=File(open(dest_path_poster, 'rb')))
        os.remove(dest_path_gif)
        os.remove(dest_path_poster)







