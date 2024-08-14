import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
GPT_API_KEY = os.environ.get('GPT_API_KEY')

current_path = os.getcwd()
soundfile_path = os.path.join(current_path, '..\\..\\soundfile')
audioFile_path = os.path.join(soundfile_path, 'soundfile.wav')

client = OpenAI(
  api_key=GPT_API_KEY
)

audio_file= open(audioFile_path, "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
print(transcription.text)