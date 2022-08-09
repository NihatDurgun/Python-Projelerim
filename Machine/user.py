#Data oluşturma Modülü
import cv2
import numpy as np
import camera
import os
from PIL import Image

camera_dec = cv2.CascadeClassifier("/home/endkng/MachineV2.0/Detection/haarcascade_frontalcamera_default.xml")
def create_new():
    cam = cv2.VideoCapture(0)
    print("User save action is starting !")
    user_id = input("Enter Your Name:")
    camera.create_user(False)
    ucount = open('Recognizer/usercount.txt',"r")
    counter = ucount.readlines()
    ucount.close()
    ucount = open('Recognizer/usercount.txt',"w")
    if(len(counter) == 0  ):
                count = 0
    else:
                count = int(counter[0])
    sampleNum = count * 10;
    count = int(count) + 1
    ucount.write(str(count))
    ucount.close()
    while (True):
        ret,img = cam.read()
        cv2.imshow("Register [<<Camera>>] Panel",img)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        cameras=camera_dec.detectMultiScale(gray,1.3,5);
        for (x,y,w,h) in cameras:
            sampleNum = sampleNum +1;
            cv2.imwrite("Users/"+str(sampleNum) +".jpg",gray[y:y+h,x:x+h])
            cv2.rectangle(img,(x,y) ,(x+w,y+h),(0,0,255),2)
            cv2.waitKey(1)
        if(sampleNum  > ((count*10) - 1)):
            camera.create_user(False)
            file = open('Recognizer/users.txt',"r")
            users = file.readlines();
            txtcount = len(users) 
            file.close()
            file = open('Recognizer/users.txt',"w") 
            users.append(str(user_id)+"_"+str(count*10)+"_"+str((count+1) * 10));
            i = 0
            for f in users:
                if(i > txtcount):
                    file.write(str("\n"+f))
                else:
                    file.write(str(f))
                i = i + 1
            file.close()
            cam.release()
            cv2.destroyAllWindows()
            print("User save to succes !")
            camera.open_camera()
            break
            
def open_camera():
    global create_status

    while True:
        result,img= cap.read()
        if create_status == True:
            tuser = thread.Thread(target=user.create_new,args=(cap,img))
            tuser.deamon=True
            tuser.start()
            create_status = False
        if status == True:
            cap ,img = watching(cap,img)
        cv2.imshow("Register[<<Camera>>] Panel",img)
        if cv2.waitKey(30) & 0xff == 27 :
           close_camera(cap)
           break

def start_trainer():
    recognizer = cv2.camera.createLBPHcameraRecognizer()
    path ='Users';
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    cameras = []
    IDs = []
    for imagePath in imagePaths:
        cameraImg = Image.open(imagePath).convert('L');
        cameraNp  = np.array(cameraImg,"uint8")
        ID = int(os.path.split(imagePath)[-1].split('.')[0])
        cameras.append(cameraNp)
        print(ID);
        IDs.append(ID)
        cv2.imshow("|<<<Training>>>|",cameraNp)
        cv2.waitKey(10)
    recognizer.train(cameras,np.array(IDs))
    recognizer.save('Recognizer/trainningData.yml')
    cv2.destroyAllWindows()

































