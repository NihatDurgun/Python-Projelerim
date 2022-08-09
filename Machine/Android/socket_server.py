import socket
import cv2
import numpy as np

status = True
server = None

def start_server():
    global status,server
    server = socket.socket()
    host_name= "192.168.1.3"
    port = 12347
    print("Your connection ip and port: "+str(host_name)+":"+str(port))
    server.bind((host_name,port))

    server.listen(1)
    while status:
        connect,name = server.accept()
        client_name = str(name)
        print(client_name.upper()+" is connected to system")
        data_recv(connect)
##      img =send_capture()
##      connet.send(img.encode())

def data_recv(connect):
    while True:
        data= connect.recv(2048)
        if data != "":
             np_array=np.fromstring(data, dtype='>f4').ravel()
             
             cv2.imshow("Data",np_array)
             if cv2.waitKey(30) & 0xff == 27 :
                break

def send_capture():
    cap = cv2.VideoCapture()
    while True:
        return img


def close_service():
    global status,server
    status = False
    server.close()
    

def open_service():
    global status
    status = True
    print("Android connection server is opening...")
    start_server()

