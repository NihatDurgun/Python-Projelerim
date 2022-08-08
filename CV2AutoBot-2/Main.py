from ppadb.client import Client as AdbClient
from skimage.measure import compare_ssim
from PIL import Image
import glob
import cv2
import pytesseract
import time
import math
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

import locale
import re
from array import *
locale.setlocale(locale.LC_ALL, 'tr_TR.utf8')

WAIT_TIME =20

HOME_BUTTON = [107,1565]
ORDERBY_CREDIT_BUTTON = [231,485]
ORDERBY_SECOND_BUTTON = [667,485]
STARTCURRENTVIDEO_BUTTON = [448,814]
OK_BUTTON = [451,1008]

MENU_BUTTON = [843,96]
LOGIN_BUTTON = [76,633]

USERNAME_INPUT=[157,479]
PASS_INPUT=[157,660]
REMEMBER_ME_BUTTON=[95,748]
LOGINCOMPLETED_BUTTON=[454,822]

VIDEO1_IMAGE = [86, 693, 171, 749]
VIDEO2_IMAGE = [300, 693, 385, 749]
VIDEO3_IMAGE = [514, 693, 599, 749]
VIDEO4_IMAGE = [728, 693, 813, 749]

VIDEO1_TEXT = [30, 760, 241, 1071]
VIDEO2_TEXT = [241, 760, 455, 1071]
VIDEO3_TEXT = [455, 760, 668, 1071]
VIDEO4_TEXT = [668, 760, 890, 1071]
"""
client = AdbClient(host="127.0.0.1", port=5037)
device = client.device("localhost:5555")
"""
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ClearAppData():
    device.shell("pm clear com.vidoix")
    
def CheckUpdateButton():
    device.shell("screencap -p /sdcard/screencap.png")
    device.pull("/sdcard/screencap.png", "screencap.png")
    img = Image.open("screencap.png")

    img2 = img.crop((550, 917, 653, 968)) #Standart Version
    #img2 = img.crop((86, 528, 171, 584)) #Premium Version
    img2.save("img2.png")

    image = cv2.imread("img2.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite("test.png", gray)

    imgEdited = Image.open("test.png")
    text = pytesseract.image_to_string(imgEdited)
   
    if("iPTAL" in text):
        print("Güncelleme bildirimi var")
        return 1
    else:
        print("Güncelleme bildirimi yok")
        return 0

def CompareText(X):
    file1 = open('spam.txt', 'r',encoding="utf-8") 
    Lines = file1.readlines() 

    for line in Lines:
        line = line.replace("\n", "")
        if(line in X):
            print("Bu video spam bir videodur!")
            return 1
    return 0
            

def StartLogin():
    device.shell("input tap "+str(MENU_BUTTON[0])+" "+ str(MENU_BUTTON[1]))
    time.sleep(4)
    device.shell("input tap "+str(LOGIN_BUTTON[0])+" "+ str(LOGIN_BUTTON[1]))
    time.sleep(10)
    device.shell("input tap "+str(USERNAME_INPUT[0])+" "+ str(USERNAME_INPUT[1]))
    device.shell("input text 'NihatDurgun'")
    time.sleep(2)
    device.shell("input tap "+str(PASS_INPUT[0])+" "+ str(PASS_INPUT[1]))
    device.shell("input text 'End.67920.end'")
    time.sleep(2)
    device.shell("input tap "+str(REMEMBER_ME_BUTTON[0])+" "+ str(REMEMBER_ME_BUTTON[1]))
    time.sleep(4)
    device.shell("input tap "+str(LOGINCOMPLETED_BUTTON[0])+" "+ str(LOGINCOMPLETED_BUTTON[1]))

def CheckCanConnected():
    device.shell("screencap -p /sdcard/screencap.png")
    device.pull("/sdcard/screencap.png", "screencap.png")
    img = Image.open("screencap.png")
    img2 = img.crop((376, 650, 522, 800))
    img2.save("img2.png")

    image = cv2.imread("img2.png")
    checker = cv2.imread("connectedchecker.png")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_orig = cv2.cvtColor(checker, cv2.COLOR_BGR2GRAY)
    
    (score, diff) = compare_ssim(gray_orig, gray, full=True)
    diff = (diff * 255).astype("uint8")
    print("CheckCanConnected: {}".format(score))

    if(score > 0.80):
        return 0
    else:
        return 1


def Test():
    device.shell("screencap -p /sdcard/screencap.png")
    device.pull("/sdcard/screencap.png", "screencap.png")
    img = Image.open("screencap.png")

def ReadTest():
    image = cv2.imread("screencap.png")
    width = int(image.shape[1] * 5)
    height = int(image.shape[0] * 5)
    dim = (width, height)
    # resize image
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gray = cv2.medianBlur(gray, 5)
    gray = cv2.Canny(gray,100,200)
    cv2.imwrite("test.png", gray)


    imgEdited = Image.open("test.png")
    text = pytesseract.image_to_string(imgEdited)
    text = text.replace("\n", " ")
    try:
        text = text.split("önce")[1]
    except:
        pass
    text = text.lstrip()
    text = re.sub(' +', ' ', text)
    print(text)
    return text

def GetName(img,x1,y1,x2,y2):
    img2 = img.crop((x1, y1, x2, y2))
    img2.save("img2.png")

    image = cv2.imread("img2.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite("test.png", gray)

    imgEdited = Image.open("test.png")
    text = pytesseract.image_to_string(imgEdited,lang="tur")
    text = text.replace("\n", " ")
    text = text.split("önce")[1]
    text = text.lstrip()
    text = re.sub(' +', ' ', text)
    print(text)
    return text


def CheckVideoAvailable():
    w, h = 2,4;
    result = [[0 for x in range(w)] for y in range(h)] 
    for ID in range(1,5):
        device.shell("screencap -p /sdcard/screencap.png")
        device.pull("/sdcard/screencap.png", "screencap.png")
        img = Image.open("screencap.png")
        img2 = img
        if(ID == 1):
            img2 = img.crop((VIDEO1_IMAGE[0], VIDEO1_IMAGE[1], VIDEO1_IMAGE[2], VIDEO1_IMAGE[3]))
            Name = GetName(img,VIDEO1_TEXT[0],VIDEO1_TEXT[1],VIDEO1_TEXT[2],VIDEO1_TEXT[3])
        elif(ID == 2):
            img2 = img.crop((VIDEO2_IMAGE[0], VIDEO2_IMAGE[1], VIDEO2_IMAGE[2], VIDEO3_IMAGE[3]))
            Name = GetName(img,VIDEO2_TEXT[0],VIDEO2_TEXT[1],VIDEO2_TEXT[2],VIDEO2_TEXT[3])
        elif(ID == 3):
            img2 = img.crop((VIDEO3_IMAGE[0], VIDEO3_IMAGE[1], VIDEO3_IMAGE[2], VIDEO3_IMAGE[3]))
            Name = GetName(img,VIDEO3_TEXT[0],VIDEO3_TEXT[1],VIDEO3_TEXT[2],VIDEO3_TEXT[3])
        elif(ID == 4):
            img2 = img.crop((VIDEO4_IMAGE[0], VIDEO4_IMAGE[1], VIDEO4_IMAGE[2], VIDEO4_IMAGE[3]))
            Name = GetName(img,VIDEO4_TEXT[0],VIDEO4_TEXT[1],VIDEO4_TEXT[2],VIDEO4_TEXT[3])
        img2.save("img2.png")

        image = cv2.imread("img2.png")
        checker = cv2.imread("checker.png")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_orig = cv2.cvtColor(checker, cv2.COLOR_BGR2GRAY)
        
        (score, diff) = compare_ssim(gray_orig, gray, full=True,multichannel=True)
        diff = (diff * 255).astype("uint8")
        print("CheckVideo"+str(ID)+"Available: {}".format(score))
        isSpam = CompareText(Name)
        print(isSpam)
        if(score > 0.45 or isSpam == 1):
            result[ID-1][0] = 0
        else: 
            result[ID-1][0] = 1
        result[ID-1][1] = Name

    return result



def ShutdownAndWaitProtocol():
    ForceStopApp()
    ClearAppData()
    time.sleep(60)

def CheckAnyAvaibleVideo():
    device.shell("screencap -p /sdcard/screencap.png")
    device.pull("/sdcard/screencap.png", "screencap.png")
    img = Image.open("screencap.png")

    img2 = img.crop((341, 646, 558, 713)) #Standart Version
    #img2 = img.crop((86, 528, 171, 584)) #Premium Version
    img2.save("img2.png")

    image = cv2.imread("img2.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite("test.png", gray)

    imgEdited = Image.open("test.png")
    text = pytesseract.image_to_string(imgEdited)
    if("Daha fazla video yiikle" in text):
        print("Izlenecek bir video bulunamadi!")
        return 0
    else:
        print("Giris Basarili!")
        return 1
    

def CheckAnyWarning():
    device.shell("screencap -p /sdcard/screencap.png")
    device.pull("/sdcard/screencap.png", "screencap.png")
    img = Image.open("screencap.png")

    img2 = img.crop((160, 808, 733, 930)) #Standart Version
    #img2 = img.crop((86, 528, 171, 584)) #Premium Version
    img2.save("img2.png")

    image = cv2.imread("img2.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite("test.png", gray)

    imgEdited = Image.open("test.png")
    text = pytesseract.image_to_string(imgEdited)
    if("kredisi tiikendi" in text):
        print("Video'nun kredisi bitti!")
        return 0
    elif("kredi kazanmacaksiniz!" in text):
        print("Video'nun kaldirildi!")
        return 0
    else:
        return 1


def CheckCurrentVideo(Name):
    device.shell("screencap -p /sdcard/screencap.png")
    device.pull("/sdcard/screencap.png", "screencap.png")
    img = Image.open("screencap.png")
    img2 = img.crop((202, 610, 436, 650)) #Standart Version
    #img2 = img.crop((769, 906, 843, 1093)) #Premium Version
    #img2 = img.crop((759, 906, 843, 955))
    
    img2.save("img2.png")

    image = cv2.imread("img2.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite("test.png", gray)

    imgEdited = Image.open("test.png")
    text = pytesseract.image_to_string(imgEdited,lang="tur")
    text = text.replace("\n", " ")
    text = text.lstrip()
    text = re.sub(' +', ' ', text)
    
    if("Video kullanılamıyor" in text):
        file = open("spam.txt","a",encoding="utf-8")
        file.write(str(Name)+"\n") 
        file.close()
        
        print("VIDEO: "+str(text)+" SPAM LISTESINE EKLENDI!")

        return 0
    else:
        return 1


def CheckVideoSeconds():
    #device.shell("screencap -p /sdcard/screencap.png")
    #device.pull("/sdcard/screencap.png", "screencap.png")
    img = Image.open("screencap.png")
    img2 = img.crop((760, 1050, 845, 1088)) #Standart Version
    #img2 = img.crop((769, 906, 843, 1093)) #Premium Version
    #img2 = img.crop((759, 906, 843, 955))
    
    img2.save("img2.png")

    image = cv2.imread("img2.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite("test.png", gray)

    imgEdited = Image.open("test.png")
    text = pytesseract.image_to_string(imgEdited,config="-c tessedit_char_whitelist=0123456789/:")
    text = text.replace('\n','')
    data = text.split("/")
    print("Videonun Toplam Süresi: "+str(data[0])+" Geçen Süre: "+str(data[1]))

    if(int(data[0]) > 0):
        return [1,int(data[0]),int(data[1])]
    else:
        return [0,None,None]
    
def AllowWarning():
    device.shell("input tap "+str(OK_BUTTON[0])+" "+ str(OK_BUTTON[1]))

def Refresh():
    device.shell("input tap "+str(HOME_BUTTON[0])+" "+ str(HOME_BUTTON[1]))

def OrderByCoin():
    device.shell("input tap "+str(ORDERBY_CREDIT_BUTTON[0])+" "+ str(ORDERBY_CREDIT_BUTTON[1]))

def OrderBySecond():
    device.shell("input tap "+str(ORDERBY_SECOND_BUTTON[0])+" "+ str(ORDERBY_SECOND_BUTTON[1]))
    
def StartVideo(x1,y1):
    device.shell("input tap "+str(x1)+" "+ str(y1))

def StartCurrentVideo():
    device.shell("input tap "+str(STARTCURRENTVIDEO_BUTTON[0])+" "+ str(STARTCURRENTVIDEO_BUTTON[1]))

def TapCancelButton():
    device.shell("input tap 599 946")
    
def WaitLoading():
    time.sleep(WAIT_TIME)


def StartApp():
    device.shell("monkey -p com.vidoix 1")

def ForceStopApp():
    device.shell("am force-stop com.vidoix")

#CheckAnyWarning()
#result = CheckVideoSeconds()

"""
while(1):
    ForceStopApp()
    ClearAppData()
    StartApp()
    time.sleep(10)
    result = CheckUpdateButton()
    if(result == 1):
        TapCancelButton()
        time.sleep(10)
    StartLogin()
    WaitLoading()
    result = CheckCanConnected()
    if(result == 1):
        try:
            while(1):
                result = CheckAnyAvaibleVideo()
                if(result == 1):
                    OrderByCoin()
                    WaitLoading()
                    result = CheckVideoAvailable()
                    willStart = -1
                    for i in range(0,4):
                        if(result[i][0] == 1):
                            print(str(i+1)+"'inci video basliyor!")
                            willStart = i+1
                            break
                    if(willStart != -1):
                        if(willStart == 1):
                            StartVideo(VIDEO1_IMAGE[0],VIDEO1_IMAGE[1])
                        elif(willStart == 2):
                            StartVideo(VIDEO2_IMAGE[0],VIDEO2_IMAGE[1])
                        elif(willStart == 3):
                            StartVideo(VIDEO3_IMAGE[0],VIDEO3_IMAGE[1])
                        elif(willStart == 3):
                            StartVideo(VIDEO3_IMAGE[0],VIDEO3_IMAGE[1])
                        WaitLoading()
                        StartCurrentVideo()
                        time.sleep(10)
                        result = CheckCurrentVideo(result[willStart-1][1])
                        if(result == 1):
                            WaitLoading()
                            result = CheckVideoSeconds()
                            if(result[0] == 1):
                                for i in range(0,round(int(int(result[2])-int(result[1]))/WAIT_TIME)):
                                    WaitLoading()
                                    result = CheckAnyWarning()
                                    if(result == 0):
                                        break
                        Refresh()
                        WaitLoading()
                    else:
                        Refresh()
                        WaitLoading()
                else:
                    print("Shutdown and Wait Protocol Uygulaniyor 1 Dakika sistem bekletilecek!")
                    ShutdownAndWaitProtocol()
                    break            
        except Exception as e:
            print("Uyari Hata ile Karsilasildi")
            print(e)
            ForceStopApp()
            time.sleep(10)
"""
