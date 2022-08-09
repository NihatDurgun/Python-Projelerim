import socket
import speech
import answer
import admin
from multiprocessing import Queue
import cameraserver
import threading as thread
port = 5000
q = Queue()
server = 0
clientsocket=0
ipadress=socket.gethostname()
def startserver():
    global port,ipadress,server
    port = 5000
    ipadress=socket.gethostname()
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    realip = str(ipadress)+":"+str(port)
    server.bind((ipadress,port))
    server.listen(80)
    print("Computer Server Start at %s And Port İs %s" %(ipadress,port))
    serverlisten()

def serverlisten():
    global server,ipadress,port,clientsocket,login
    while True:
        (clientsocket,adress) = server.accept()
        print("Connection From: " + str(adress))
        msg = "Welcome my server!"
        ssl = thread.Thread(target=listenchat)
        ssl.daemon = True
        ssl.start()
        sendmessage(msg)
        
def listenchat():
    global clientsocket,login
    while True:
        #Receiving from client
        data = clientsocket.recv(1024)
        'OK...' + data.decode('utf-8')
        x1,x2,x3 = answer.makeanswer(data.decode("utf-8"))
        if(x3 == True):
            start(x1)
        speech.talk(x2)
        print("ADMIN: "+data.decode('utf-8'))
        if not data: 
         break

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

def start(text):
    eval(text)
    
def sendmessage(msg):
    clientsocket.send(msg.encode('utf-8'));
    print("\nCOMPUTER[ME}: "+msg)
