import pvporcupine
import pyaudio
from config import access_key, wake_word_model_path

# Create an instance of Porcupine with the custom wake word model
porcupine = pvporcupine.create(access_key=access_key, keyword_paths=[wake_word_model_path])

# Set up audio input stream
audio_stream = pyaudio.PyAudio().open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

# Continuously process audio frames
while True:
    pcm = audio_stream.read(porcupine.frame_length)
    pcm = pcm.flatten().astype(float)

    # Process the audio frame and check for the wake word
    keyword_index = porcupine.process(pcm)

    if keyword_index >= 0:
        # Wake word detected, trigger your AI to respond here
        print("Wake word detected!")