import numpy as np
import cv2
import os
import user
from multiprocessing import Queue
import threading as thread
import math
osdir = os.path.dirname(os.path.realpath(__file__))
face_dec = cv2.CascadeClassifier(osdir+"\\Detection\\haarcascade_frontalface_default.xml")
hand_dec = cv2.CascadeClassifier(osdir+"\\Detection\\palm.xml")
status = True
create_status = False

rec = cv2.face.createLBPHFaceRecognizer();
rec.load("Recognizer\\trainningData.yml");
Id = 0;
font  = cv2.FONT_HERSHEY_COMPLEX_SMALL
trainer = []
def watching(img):
        global font
        gray  = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = face_dec.detectMultiScale(gray,1.3,5)
        hands = hand_dec.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),((x+w),(y+h)),(0,255,255),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            Id ,conf = rec.predict(roi_gray)
            name = findID(Id)
            if (name[0:2] == "\n" ):
                 name = name[2:]
            cv2.putText(img,str(name),(x,y+h),font,1.5,(0,255,255),2,cv2.LINE_AA);
        for (x,y,w,h) in hands:
                 cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,255,255),2)
                 roi_gray = gray[y:y+h, x:x+w]
                 roi_color = img[y:y+h, x:x+w]
        return img

def make_trainer():
    global trainer
    file  = open('Recognizer\\users.txt',"r")
    users = file.readlines()
    for vb in  users:
        vbedit = vb.split('_')
        trainer.append(vbedit)
        
def findID(Id):
    det = Id/ 10;
    det = math.floor(det)
    name = trainer[int(det)][0]
    return name
q = Queue()
def open_camera():
    global create_status
    make_trainer()
    cap = cv2.VideoCapture(0)
    print("Camera Module is opening...")
    while True:
        result,img= cap.read()
        if create_status == True:
            close_camera(cap)
            tuser = thread.Thread(target=user.create_new)
            tuser.deamon=True
            tuser.start()
            create_status = False
        if status == True:
           img = watching(img)
        cv2.imshow("Admin [<<Camera>>] Panel",img)
        if cv2.waitKey(30) & 0xff == 27 :
           close_camera(cap)
           break
def servercamera(frame):
        create_status=False
        status=False
        print("Camera Module is opening...")
        while True:
                if create_status == True:
                    tuser = thread.Thread(target=user.create_new)
                    tuser.deamon=True
                    tuser.start()
                    create_status = False
                if status == True:
                    videoframe = watching(frame)
                cv2.imshow("Admin [<<Camera>>] Panel",frame)
                if cv2.waitKey(30) & 0xff == 27 :
                   close_camera(cap)
                   break
        
def create_user(status):
        global create_status
        create_status = status
def face_detect(stat):
    global status
    status = stat

def close_camera(cap):
    print("Camera Module is closing...")
    cap.release()
    cv2.destroyAllWindows()

