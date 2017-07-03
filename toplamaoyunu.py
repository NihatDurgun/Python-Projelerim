from random import randint
def soru(kademe = 0):
    if(kademe >= 0):
        x1 = randint(0,10*kademe)
        x2 = randint(0,10*kademe)
        print(str(x1) + "+" + str(x2) + "= ?")
    else:
        x1 = randint(10 * kademe,0)
        x2 = randint(10 * kademe,0)
        print(str(x1) + str(x2) + "= ?")
    if(int(input("CEVAP: ")) == x1 + x2):
        print("Doğru Cevap!")

while(True):
    kademe = input("Kademe Giriniz (İstenilen Sayı Girilebilir): ")
    soru(int(kademe))
    drm = str(input("Devam Etmek İstermisiniz: "))
    if(drm == "H" and drm == "h"):
        break