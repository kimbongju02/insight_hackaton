
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from . import openai_api, eleven_api
from django.http import FileResponse

input_audiofile = settings.PATH.get('INPUT_AUDIOFILE')
output_audiofile = settings.PATH.get('SAVE_TTS_FILE')

@csrf_exempt
def upload_audio(request):
    if request.method == 'POST':
        audio_file = request.FILES['audio_file']
        with open(input_audiofile, 'wb') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)
        openai_api.stt()
        message = openai_api.text_generation()
        eleven_api.tts(message)

        response = FileResponse(open(output_audiofile, 'rb'))

        return response