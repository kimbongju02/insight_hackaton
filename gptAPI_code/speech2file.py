import queue, os, threading
import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write
import time

current_path = os.getcwd()
save_soundFile_path = os.path.join(current_path, "..\\..\\soundfile")
if not os.path.exists(save_soundFile_path):
    os.makedirs(save_soundFile_path, exist_ok=True)
save_soundFile_name = os.path.join(save_soundFile_path, "soundfile.wav")

q = queue.Queue()
recorder = False
recording = False

def complicated_record():
    with sf.SoundFile(save_soundFile_name, mode='w', samplerate=16000, subtype='PCM_16', channels=1) as file:
        with sd.InputStream(samplerate=16000, dtype='int16', channels=1, callback=complicated_save):
            while recording:
                file.write(q.get())
        
def complicated_save(indata, frames, time, status):
	q.put(indata.copy())
    
def start():
    global recorder
    global recording
    
    recording = True
    recorder = threading.Thread(target=complicated_record)
    print('start recording')
    recorder.start()
    
def stop():
    global recorder
    global recording

    recording = False
    recorder.join()
    print('stop recording')
    
start()
time.sleep(3)
stop()