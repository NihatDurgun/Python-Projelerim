import socket
import speech
import answer
from multiprocessing import Queue
import threading as thread
import camera
import binascii
import cv2
import numpy as np
port = 5001
q = Queue()
server = 0
clientsocket=0
ipadress=socket.gethostname()

def startserver():
    global port,ipadress,server
    port = 5001
    ipadress=socket.gethostname()
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    realip = str(ipadress)+":"+str(port)
    server.bind((ipadress,port))
    server.listen(80)
    print("Computer Server Start at %s And Port İs %s" %(ipadress,port))
    serverlisten()

def serverlisten():
    global server,ipadress,port,clientsocket
    while True:
        (clientsocket,adress) = server.accept()
        print("Connection From: " + str(adress))
        ssl = thread.Thread(target=listenchat)
        ssl.daemon = True
        ssl.start()

def listenchat():
    global clientsocket
    s = ""
    while True:
        data =""
        image_str =""
        image_decoded =None
        data += clientsocket.recv(46080)
        byte += data
        try:
            image_str = str(data,'utf-8')
            image_decoded = np.fromstring(image_str, np.uint8)
            img = np.reshape(image_decoded, (120, 120, 2))
            cv2.imshow("image",img)
        except Exception:
            print(len(data))

        
        
def start(text):
    eval(text)
    
def sendmessage(msg):
    clientsocket.send(msg.encode('utf-8'));
    print("CAMERA COMPUTER[ME}: "+msg)
