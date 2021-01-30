from pathlib import Path
from moviepy.video.io.VideoFileClip import VideoFileClip
from django.core.files import File
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def update_gif_poster(instance, title, video):

    dest_file_name_gif = str(title) + '.gif'
    dest_file_name_poster = str(title) + '.png'

    dest_path_gif = f'{BASE_DIR}/media/gifs/{dest_file_name_gif}'
    dest_path_poster = f'{BASE_DIR}/media/posters/{dest_file_name_poster}'

    poster = VideoFileClip(f'{BASE_DIR/video.temporary_file_path()}').save_frame(dest_path_poster, t=0.00)
    gif = VideoFileClip(f'{BASE_DIR/video.temporary_file_path()}').subclip(0, 2).write_gif(dest_path_gif)

    instance.gif.save(f'{dest_file_name_gif}', content=File(open(dest_path_gif, 'rb')))
    instance.poster.save(f'{dest_file_name_poster}', content=File(open(dest_path_poster, 'rb')))
    os.remove(dest_path_gif)
    os.remove(dest_path_poster)






