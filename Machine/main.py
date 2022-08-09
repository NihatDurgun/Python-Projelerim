import speech
import camera,user
import server,cameraserver
from multiprocessing import Queue
import threading as thread
import answer
import smservice
from urllib.request import urlopen
import urllib

def check_int():
    try:
        response = urlopen('https://www.google.com',timeout=1)
        return True
    except urllib.error.URLError:
        return False

connect = check_int()
def op_cam():
    q.put(camera.open_camera())

def op_spk():
   q.put(set_spk())

def set_spk():
    global connect
    print(connect)
    speech.open_speak(connect)
    while True:
        code = False
        iscode = None
        text = speech.return_dialog(connect)
        code,iscode = speech_answer.answer(text)
        if iscode == True:
            to_code(code)
        
def to_code(code):
    eval(code)

def sms():
    smservice.open_service()
    q.put(phone_service())

def phone_service():
    while True:
        sms = smservice.sms_notify()
        code,text,iscode =sms_answer.answer(sms)
        try:
            if iscode == True:
                to_code(code)
            else:
                print(text)
            smservice.send_sms("Your job is working !")
            
        except NameError:
            smservice.send_sms("Your job is not working ! ")
        except AttributeError:
            smservice.send_sms("Your job is working ! ")

def op_socketserver():
    server.startserver()
    
def startcamera():
    try:
        socket = thread.Thread(target=camera_socketserver)
        socket.deamon = True
        socket.start()
        print("INFO:Socket Server İs Opening!")
    except:
        print("INFO:Socket Server Başlatılma Hatası")

def camera_socketserver():
    cameraserver.startserver()

def socketserver():
    try:
        socket = thread.Thread(target=op_socketserver)
        socket.deamon = True
        socket.start()
        print("INFO:Socket Server İs Opening!")
    except:
        print("INFO:Socket Server Başlatılma Hatası")
        
q = Queue()
def main():
    try:
        camera.face_detect(True)
        cam = thread.Thread(target=op_cam)
        cam.daemon = True
        cam.start()
    except:
        print("INFO:OpenCV Camera Başlatılma Hatası")
    try:
        spk = thread.Thread(target=op_spk)
        spk.deamon=True
        spk.start()
    except:
        print("INFO:Speech Module Başlatılma Hatası")
    try:
        onsms = thread.Thread(target=sms)
        onsms.deamon=True
        onsms.start()
    except:
        print("INFO:Twilio Server Başlatılma Hatası")
    try:
        socket = thread.Thread(target=op_socketserver)
        socket.deamon = True
        socket.start()
        print("INFO:Socket Server İs Opening!")
    except:
        print("INFO:Socket Server Başlatılma Hatası")

def close():
    camera.close_camera()
    speech.close_speak()
    smservice.close_service()
