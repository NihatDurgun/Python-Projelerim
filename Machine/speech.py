import speech_recognition as speech
from gtts import gTTS
import time
from subprocess import call
import os
import espeak
from multiprocessing import Queue
import threading as thread
from urllib.request import urlopen
import urllib
path = ""
rec = speech.Recognizer()
mic = speech.Microphone()
ftime =True
dialog = ""
trackerpath = os.path.dirname(os.path.realpath(__file__)) +"\\Tracker\\"
osdir = os.path.dirname(os.path.realpath(__file__))
def talk(text):
    if check_int():
        google_talk(text)
    else:
        espeak_talk(text)

def google_talk(text):
    global path
    path =trackerpath +text+".wav"
    print(path)
    if not(os.path.isfile(path)):
        tts = gTTS(text=text,lang = "en")
        tts.save(path)
        call([osdir+"\\VLC\\vlc.exe","--play-and-exit",path])
    time.sleep(1.5)

def espeak_talk(text):
    es = espeak.ESpeak()
    es.say(text)
    time.sleep(1.5)

def check_int():
    try:
        response= urlopen('https://www.google.com',timeout=1)
        return True
    except urllib.error.URLError:
        return False

def false_int():
    global ftime,rec
    if ftime == True:
        with mic as source:
            rec.adjust_for_ambient_noise(source)
            print("Set Minimum Threshold To {}".format(rec.energy_threshold))
            ftime = False
            espeak_talk("I am ready to speak")
            print("INFO: I am ready to speak")
        
def true_int():
    global ftime,rec
    if ftime == True:
        with mic as source:
            rec.adjust_for_ambient_noise(source)
        print("Set Minimum Threshold To {}".format(rec.energy_threshold))
        if not(os.path.isfile(trackerpath+"fstart.wav")):
            tts = gTTS(text="I am ready to speak",lang ="en")
            tts.save(trackerpath+"fstart.wav")
        google_talk("fstart")
        print("INFO: I am ready to speak")
        ftime = False
        
def return_dialog(connect_int):
    global status,rec
    if connect_int == True:
        while status == True:
            with speech.Microphone() as source:
                audio = rec.listen(source)
            dialog = ""
            try:
                dialog = rec.recognize_google(audio)
                print("Machine thinking you said " + dialog)
            except speech.UnknownValueError:
                pass
            except speech.RequestError as e:
                print("Machine can't reach to server {0}".format(e))
            if dialog != "":
                return dialog
    else:
        while status == True:
            with speech.Microphone() as source:
                audio = rec.listen(source)
            dialog = ""
            try:
                dialog = rec.recognize_sphinx(audio)
                print("Machine thinking you said " + dialog)
            except speech.UnknownValueError:
                pass
            except speech.RequestError as e:
                print("Machine crashed:  {0}".format(e))
            if dialog != "":
                return dialog
        
        
def open_speak(check):
    global status
    status = True
    if check == True:
        print("Speak Module is opening...")
        true_int()
    else:
        print("Speak Module is opening...")
        false_int()

def close_speak():
    status = False
    print("Speak Module is closing...")
