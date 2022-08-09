__author__="Emre Nihat Durgun"

print("#################################################")  
print("\nV1.0 Dikdörtgenin Alanını Hesaplamak İçin: dortgen_alan_hesapla_v1(uzun_kenar,kisa_kenar) fonksiyonunu kullanabilirisiniz")
print("V1.0 Dairenin Alanını Hesaplamak İçin: daire_alan_hesapla_v1(yaricap) fonksiyonunu kullanabilirisiniz")
print("\n#################################################")      
print("\nV2.0 Dikdörtgenin Alanını Hesaplamak İçin: dortgen_alanı_hesapla_v2() fonksiyonunu kullanabilirisiniz")
print("V2.0 Dairenin Alanını Hesaplamak İçin: daire_alanı_hesapla_v2() fonksiyonunu kullanabilirisiniz")
print("\n#################################################")   
print("\nNOT:İkinci Durumlarda veriler input ile alındı.Ayrıyeten pi değerinin hassaslığı artırıldı!")
print("\n#################################################")

def dortgen_alan_hesapla_v1(uzun_kenar,kisa_kenar):
    print("Dikdörtgenin Alanı: "+str(uzun_kenar*kisa_kenar))

def daire_alan_hesapla_v1(yaricap):
    pi=3.14
    print("Dairenin Alanı: "+str(pi*yaricap*yaricap))

def dortgen_alanı_hesapla_v2():
    uzun_kenar=input("Lütfen Dikdörtgenin Uzun Kenarı Giriniz: ")
    kisa_kenar=input("Lütfen Dikdörtgenin Kısa Kenarı Giriniz: ")
    print("Dikdörtgenin Alanı: "+str(int(uzun_kenar)*int(kisa_kenar)))

def daire_alanı_hesapla_v2():
    yaricap=int(input("Lütfen Dairenin Yarıçapını Giriniz: "))
    pi=3.141592653589793
    print("Dairenin Alanı: "+str(pi*yaricap*yaricap))
