from gtts import gTTS
import os

from playsound import playsound

def say(text_val):
    language = 'en'
    obj = gTTS(text=text_val, lang=language, slow=False)
    obj.save("voice.mp3")
    playsound("voice.mp3")
    os.remove("voice.mp3")
        