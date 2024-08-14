from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import os
from dotenv import load_dotenv
import requests
from django.conf import settings

load_dotenv()
ELEVEN_API_KEY = os.environ.get('ELEVEN_API_KEY')

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/zrHiDhphv9ZnVXBqCLjz"

save_tts_file = settings.PATH.get('SAVE_TTS_FILE')

def tts(message):
        
    headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": ELEVEN_API_KEY,
    }

    data = {
    "text": message,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.75
    }
    }

    response = requests.post(url, json=data, headers=headers)
    print(response)
    with open(save_tts_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)