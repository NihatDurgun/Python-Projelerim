print("########## Emre Durgun Tarafından Yapıldı ##########")
from random import randint
def faktroyel(sayı):
    if (sayı == "R" or sayı == "r"):
        sayı = randint(0,100)
    else:
        sayı = int(sayı)
    toplam = 1;
    for i in range(0,sayı):
        toplam = (sayı-i) * toplam
    print("Sonuç " +str(sayı)+"!" +": " + str(toplam))

while(True):
    faktroyel(input("Faktroyel Alınacak Sayıyı Giriniz(Random için R): "))
    drm = input("Devam Etmek İstermisiniz: ")
    if (drm == "H" or drm == "h"):
        break