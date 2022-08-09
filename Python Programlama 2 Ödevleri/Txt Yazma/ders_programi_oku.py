__author__="Emre Nihat Durgun"
import os

def txtoku():
    with open(os.getcwd()+"\\ders_programi.txt","r") as file:
        data = file.readlines()
        i=0
        for line in data:
            print("Okunan Veri ["+str(i)+"]:"+str(line))
            i=i+1
    print("Okuma İşlemi Sonlandırıldı!")


print("ders_programi.txt Adlı Dosya İçin Okuma İşlemi Başlatıldı!")
txtoku()
