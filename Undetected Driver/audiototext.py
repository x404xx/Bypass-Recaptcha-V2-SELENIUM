import os
from time import sleep
from colortext import *
from pydub import AudioSegment
from urllib.request import urlretrieve
from speech_recognition import Recognizer, AudioFile

def audioText(audio_source):
    #! Download Audio
    urlretrieve(audio_source, f'{os.getcwd()}\\audio.mp3')
    sleep(3)
    AudioSegment.from_mp3(f'{os.getcwd()}\\audio.mp3').export(f'{os.getcwd()}\\audio.wav', format='wav')
    sample_audio = AudioFile(f'{os.getcwd()}\\audio.wav')

    #! Translate Audio To Text
    recog = Recognizer()
    with sample_audio as source:
        audio = recog.record(source)
    phrase = recog.recognize_google(audio)
    print(f'{INFO} {purple}Phrase Text{reset} {red}>{reset} {green}{phrase}{reset}')
    return phrase