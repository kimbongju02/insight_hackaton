from django.urls import path

from . import views, speech_to_file

urlpatterns = [
    path('', views.index),
    path('upload_audio', speech_to_file.upload_audio),
]