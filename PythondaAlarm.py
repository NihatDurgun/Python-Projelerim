print("*****Bu Program Emre Durgun Tarafından Yapılmıştır!*****")
import time
saat=0
gün=0
ay=0
yıl=0
kontrol = False
def alarmkur():
    global saat,gün,ay,yıl,kontrol
    print("#####Girilecek Değerler Sayı Bazında Olacaktır#####")
    saat = int(input("Alarm Kurulacak Saat Girin: "))
    gün = int(input("Alarm Kurulacak Gün Girin: "))
    ay =  int(input("Alarm Kurulacak Ay Girin: "))
    yıl =  int(input("Alarm Kurulacak Yıl Girin: "))
    alarmkontrol()

def alarmkontrol():
    global kontrol,saat,gün,ay,yıl
    print("Alarm Çalıcak Saat: " + str(saat)+" "+str(gün)+"/"+str(ay)+"/"+str(yıl))
    while(kontrol ==False):
        if(saat == int(time.strftime("%H")) and gün == int(time.strftime("%d")) and  ay == int(time.strftime("%m")) and yıl == int(time.strftime("%Y")) ):
            i=0
            while(i<10):
                print("ALARM !")
                i=i+1
                kontrol =  True
alarmkur()