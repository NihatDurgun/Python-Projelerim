import socket
import cv2

status = True
client = None
def start_client(host_name,port):
    global status,client
    client = socket.socket()
    host_name = "192.168.1.3"
    port=12347

    client.connect((host_name,port))
    while status:
        msg= client.recv(1024)
        cv2.imshow("Android Screen <<"+hostname":"+port+">>",msg.decode())

def close_client():
    global status,client
    status = False
    client.close()

def open_service(host_name,port):
    global status
    print("Android client service is opening...")
    start_client(host_name,port)


