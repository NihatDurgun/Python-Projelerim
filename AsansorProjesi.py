# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 19:15:38 2020

@author: YağızhanŞimşek
"""

#mod, kat, hedef, doluluk, [kişi sayısı, kat]
import numpy as np
import time
import _thread
class Kat:
    def __init__(self):
        self.toplam=0
        self.sira=np.zeros(5,dtype=int)
    def SirayaEkle(self,idx, sayi):
        self.sira[idx] += sayi
    def Sira(self):
        return self.sira
class Asansor:
    def __init__(self):
        self.mod = False
        self.kat = 0
        self.hedef = 0
        self.yon=True
        self.max = 10
        self.doluluk = 0
        self.icerik = np.zeros(5)
    def Reset(self):
        self.__init__()
    def Dongu(self):
        while True:
            if(self.mod == False and self.kat == 0):
                continue
            """
            Yön yukarı ise, bulunduğun kat ve yukardaki katlara bak.
            En yukardaki sıraya kadar çık(kat 5 boşsa 4e kadar çık)
            Yeni gelenler olduğu için oradan aşağıya in.
            """
            #Kata çıktın
            if(self.yon == True and self.hedef > self.kat):
                self.kat += 1
            if(self.yon == False and self.hedef < self.kat):
                self.kat -= 1
            if(self.kat == len(binaKati)-1):
                self.yon = False
            if(self.kat == 0):
                self.yon = True
            if(self.yon == True):
                self.KatBosalt()
                #bulunduğun kattakileri al, hedefin içindekilerin çağırdığı en alt kat. Yukarı çıktığın için aşağı inenleri alma.
                if(self.kat == 0):
                    if(self.mod == False):
                        self.Reset()
                        continue
                    self.KatDoldur()
                for i in range(len(self.icerik) - 1, -1, -1):
                    if(self.icerik[i] != 0):
                        self.hedef = i
                #İçi boşsa, direk aşağı insin.
                if np.equal(self.icerik,np.zeros(5)).all():
                    self.hedef = 0
                    self.yon = False
                    self.KatDoldur()
            if(self.yon == False):
                self.KatBosalt()
                self.KatDoldur()

                #Hedef: aşağı yönde en yakın katta sıra bekleyenler. yoksa zemin kata in.
                for i in range(0, len(binaKati)):
                    if(not np.sum(binaKati[i].sira)==0 and i < self.kat):
                        self.hedef = i
                if self.hedef >= self.kat:
                    self.hedef = 0
            #Hata testi
            time.sleep(0.2)
    def KatBosalt(self):
        if(self.icerik[self.kat]) == 0:
            return
        self.doluluk -= self.icerik[self.kat]
        binaKati[self.kat].toplam += self.icerik[self.kat]
        self.icerik[self.kat] = 0
    def KatDoldur(self):
        sira = binaKati[self.kat].sira
        if(np.sum(sira) == 0):
            return
        for i in range(len(sira)):
            if(self.yon == True and i < self.kat):
                continue
            if (self.yon == False and i > self.kat):
                continue
            self.icerik[i] += sira[i]
            self.doluluk += sira[i]
            binaKati[self.kat].sira[i] = 0
        #Doluluk 10u geçtiyse rastgele katlardan kalan insanları boşalt
        if(self.doluluk > self.max):
            fark = int(self.doluluk - 10)
            for i in range(fark):
                for i in range(20):
                    if self.yon == True:
                        randKat = np.random.randint(1,5)
                    else:
                        randKat = 0
                    if self.icerik[randKat] != 0:
                        break
                self.icerik[randKat] -= 1
                binaKati[self.kat].sira[randKat] += 1
            self.doluluk = self.max
def Kontrol():
    while True:
        #Her bir kat için sıradaki kişi sayısını hesapla
        totalQ = 0
        totalC = 0
        for i in range(len(binaKati)):
            totalQ += np.sum(binaKati[i].Sira())
        #Toplam asansör kapasitesini hesapla
        for i in range(len(binaAsansoru)):
            if(binaAsansoru[i].mod==True):
                totalC += binaAsansoru[i].max
        if(totalQ > totalC * 2):
            for i in range(1, len(binaAsansoru)):
                if(binaAsansoru[i].mod == False):
                    binaAsansoru[i].mod = True
                    break
        if(totalQ < totalC):
            for i in range(len(binaAsansoru)-1,0,-1):
                if(binaAsansoru[i].mod==True):
                    binaAsansoru[i].mod=False
                    break
        time.sleep(0.1)
def Log():
    while True:
        input("Log için entera bas: ")
    #Katların özeti^l
        for i in range(len(binaKati)):
            if(i == 0):
                print("Kat: ",i, " Sıra: ", binaKati[i].sira, " Çıkış: ", binaKati[i].toplam)
            else:
                print("Kat: ",i, " Sıra: ",binaKati[i].sira, " Toplam: ",binaKati[i].toplam)

        #Asansörlerin Özeti
        for i in range(len(binaAsansoru)):
            a = binaAsansoru[i]
            print("Asansör No: ",i)
            if(a.mod == False):
                print("\tMod: Kapalı")
            else:
                print("\tMod: Açık")
            print("\tKat: ",a.kat)
            print("\tHedef: ",a.hedef)
            print("\tKapasite: ",a.max)
            if (a.yon == False):
                print("\tYön: Aşağı")
            else:
                print("\tYön: Yukarı")
            print("\tDoluluk: ",a.doluluk)
            print("\tİçerik: ",a.icerik)
def YeniGelen():
    while True:
        katlar = [0, 0, 0, 0, 0]
        kisiler = int(np.random.randint(1,11))
        for i in range(kisiler):
            kat = np.random.randint(1,5)
            katlar[kat] += 1
        binaKati[0].sira = np.add(binaKati[0].sira, katlar)
        time.sleep(0.5)
def Gidenler():
    while True:
        katlar = [0, 0, 0, 0, 0]
        kisiler = int(np.random.randint(1,6))
        for i in range(kisiler):
            kat = np.random.randint(1,5)
            katlar[kat] += 1
        for i in range(1,len(binaKati)):
            binaKati[i].SirayaEkle(0, katlar[i])
        time.sleep(1)

binaAsansoru = np.zeros(5, dtype=Asansor)
binaKati = np.zeros(5, dtype=Kat)
for i in range(5):
    binaAsansoru[i] = Asansor()
    binaKati[i] = Kat()
binaAsansoru[0].mod=True
_thread.start_new_thread(YeniGelen,())
_thread.start_new_thread(Gidenler,())
_thread.start_new_thread(Kontrol,())
_thread.start_new_thread(Log,())
for i in range(len(binaAsansoru)):
    _thread.start_new_thread(binaAsansoru[i].Dongu,())

while True:
    pass