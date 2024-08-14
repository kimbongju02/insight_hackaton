import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from django.conf import settings

load_dotenv()
API_KEY = os.environ.get('API_KEY')

client = OpenAI(
  api_key=API_KEY
)

input_audiofile = settings.PATH.get('INPUT_AUDIOFILE')
save_stt_file = settings.PATH.get('SAVE_STT_FILE')
save_tts_file = settings.PATH.get('SAVE_TTS_FILE')

def tts(message):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=message
    )
    response.stream_to_file(save_tts_file)
    
def stt():
    audio_file= open(input_audiofile, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    
    with open(save_stt_file, 'wt', encoding='utf-8') as f:
        f.write(transcription.text)
        
def text_generation():
    with open(save_stt_file, 'r', encoding='utf-8') as f:
        message = f.read()
    
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message}
    ]
    )
    result = response.choices[0].message.content
    return result