import os
#import wave
#import pyaudio
import numpy as np
#from scipy.io import wavfile
#import time
#from faster_whisper import WhisperModel


from voice_service import respond
from engine_create import interact_with_llm
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from load_file import data_ingestion

import speech_recognition as sr
from ffmpeg_setup import set_ffmpeg_path
import whisper
import time

source = sr.Microphone()
recognizer = sr.Recognizer()

base_model_path = os.path.expanduser('~/.cache/whisper/base.pt')
base_model = whisper.load_model(base_model_path)
#DEFAULT_CHUNK_LENGTH = 10
#STOP_SILENCE_DURATION = 2  # 2 seconds of silence to stop recording

Settings.llm = Ollama(model="llama3.2:1b")

def listen_for_command():
    
    with source as s:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        with open("command.wav", "wb") as f:
            f.write(audio.get_wav_data())
        command = base_model.transcribe("command.wav")
        if command and command['text']:
            print("You said:", command['text'])
            return command['text'].lower()
        return None
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        print("Unable to access the Google Speech Recognition API.")
        return None

"""
def transcribe_audio(model, file_path):
    segments, info = model.transcribe(file_path, beam_size=7)
    transcription = ' '.join(segment.text for segment in segments)
    return transcription
"""

def main():

    data_ingestion()
    set_ffmpeg_path()
    while True:

        command = listen_for_command()

    #transcription = transcribe_audio(model, "command.wav")

    # Process customer input and get response from AI assistant
        output = interact_with_llm(command)
        print(output)
        if output:
            respond(output)
            
        time.sleep(1)
            # Start listening again after AI responds
    #time.sleep(1)  # Small delay to ensure clean transition back to listening

if __name__ == "__main__":
    main()
