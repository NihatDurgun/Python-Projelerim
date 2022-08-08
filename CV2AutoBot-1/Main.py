from ppadb.client import Client as AdbClient
from skimage.measure import compare_ssim
from PIL import Image
import glob
import cv2
import pytesseract
import time

LOGIN_BUTTON = [444,1530]
BACK_BUTTON=[37,78]
COIN_BUTTON=[834,80]
EARNKIN_BUTTON = [643,203]
STARTAdvertisement_BUTTON = [465,460]
STOPAdvertisement_BUTTON = [837,57]


client = AdbClient(host="127.0.0.1", port=5037)
device = client.device("localhost:5565")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def Test():
    device.shell("screencap -p /sdcard/screencap.png")
    device.pull("/sdcard/screencap.png", "screencap.png")
    img = Image.open("screencap.png")

def CheckGoogleAd():
    img = Image.open("screencap.png")
    img2 = img.crop((386, 1448, 485, 1488))
    img2.save("gtest.png")
    
    image = cv2.imread("gtest.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)[1]  
    cv2.imwrite("gtest_edited.png", thresh)

    imgEdited = Image.open("gtest_edited.png")
    text = pytesseract.image_to_string(imgEdited)
    print(text)
    if(text == "Google"):
        return 1
    else:
        return 0

def CheckGoogleAdSeconds():
    img = Image.open("screencap.png")
    img2 = img.crop((551, 14, 630, 114))
    img2.save("gsecondtest.png")
    
    image = cv2.imread("gsecondtest.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)[1]  
    cv2.imwrite("gsecondtest_edited.png", thresh)

    imgEdited = Image.open("gsecondtest_edited.png")
    text = pytesseract.image_to_string(imgEdited,config="-c tessedit_char_whitelist=0123456789/:")
    text = text.replace('\n','')
    if text != "":
        return [1,int(text)]
    else:
        return [0,int(text)]

def CheckVideoSeconds():
    device.shell("screencap -p /sdcard/screencap.png")
    device.pull("/sdcard/screencap.png", "screencap.png")
    
    img = Image.open("screencap.png")
    img2 = img.crop((386, 1448, 485, 1488))
    img2.save("gtest.png")
    result = CheckGoogleAd()

    if(result == 1):
        result = CheckGoogleAdSeconds()
        if (result[0] == 1):
            print("Reklamin "+str(result[1])+" saniye sonra bitecek")
            time.sleep(result[1]+5)
            StopAdvertisement()
            

def StartAdvertisement():
    device.shell("input tap "+str(STARTAdvertisement_BUTTON[0])+" "+ str(STARTAdvertisement_BUTTON[1]))

def BACKMAIN_PAGE():
    device.shell("input tap "+str(BACK_BUTTON[0])+" "+ str(BACK_BUTTON[1]))

def StopAdvertisement():
    device.shell("input tap "+str(STOPAdvertisement_BUTTON[0])+" "+ str(STOPAdvertisement_BUTTON[1]))

def OpenEarnKIN():
    device.shell("input tap "+str(COIN_BUTTON[0])+" "+ str(COIN_BUTTON[1]))
    time.sleep(3)
    device.shell("input tap "+str(EARNKIN_BUTTON[0])+" "+ str(EARNKIN_BUTTON[1]))

def WaitLoading():
    time.sleep(10)

def WaitLogin():
    time.sleep(20)

def StartApp():
    device.shell("monkey -p io.peerbet.peerbet 1")

def ForceStopApp():
    device.shell("am force-stop io.peerbet.peerbet")

def StartLogin():
    device.shell("input tap "+str(LOGIN_BUTTON[0])+" "+ str(LOGIN_BUTTON[1]))


while(1):
    try:
        while(1):
            ForceStopApp()
            StartApp()
            time.sleep(3)
            StartLogin()
            WaitLogin()
            OpenEarnKIN()
            WaitLoading()
            StartAdvertisement()
            time.sleep(5)
            CheckVideoSeconds()
    except Exception as e:
        print("Uyari Hata ile Karsilasildi")
        print(e)
        ForceStopApp()
        StartApp()
        WaitLoading()


