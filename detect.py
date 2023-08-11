import pvporcupine
import pyaudio
from config import access_key, wake_word_model_path
import numpy as np
import sounddevice as sd

porcupine = pvporcupine.create(access_key= access_key, library_path='./lib', model_path=wake_word_model_path, keyword_paths=[wake_word_model_path])


def audio_callback(indata, frames, time, status):
    # Convert the audio data to 16-bit integer array
    pcm = (indata * 32767).astype("int16")

    # Process the audio frame and check for the wake word
    keyword_index = porcupine.process(pcm)

    if keyword_index >= 0:
        # Wake word detected, trigger your AI to respond here
        print("Wake word detected!")


# Open the audio stream and start the detection
with sd.InputStream(callback=audio_callback):
    print("Listening for wake word...")
    sd.sleep(-1)