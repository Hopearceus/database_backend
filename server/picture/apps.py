from django.apps import AppConfig

# from .models import Picture

class PictureConfig(AppConfig):
    # model = Picture
    name = 'picture'
    fields = ['pid', 'creator', 'create_time', 'image', 'file_name']