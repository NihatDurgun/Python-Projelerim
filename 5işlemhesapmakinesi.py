#Amaç:İşlem Yapan Makine

def toplama(sayı1,sayı2):
    return sayı1+sayı2;

def cikarma(sayı1,sayı2):
    return sayı1-sayı2;

def carpma(sayı1,sayı2):
    return sayı1*sayı2;

def bölme(sayı1,sayı2):
    return sayı1/sayı2;

def kalan(sayı1,sayı2):
    return sayı1%sayı2

def main():
    while(True):
        print("Operatörler = [+],[-],[*],[/],[%]")
        islem = input("İşlemi Giriniz: ");

        po = islem.find("+")
        mo = islem.find("-")
        co = islem.find("/")
        io = islem.find("*")
        ko = islem.find("%")

        try:
            if(po != -1):
                    s1 = int(islem[0:po])
                    operator = islem[po]
                    s2 = int(islem[po+1:])
            elif(mo != -1):
                    s1 = int(islem[0:mo])
                    operator = islem[mo]
                    s2 = int(islem[mo+1:])
            elif(co != -1):
                    s1 = int(islem[0:co])
                    operator = islem[co]
                    s2 = int(islem[co+1:])
            elif(io != -1):
                    s1 = int(islem[0:io])
                    operator = islem[io]
                    s2 = int(islem[io+1:])
            elif(ko != -1):
                    s1 = int(islem[0:ko])
                    operator = islem[ko]
                    s2 = int(islem[ko+1:])
            else:
                    print("Hatalı değer Girdiniz !")
        except:
            print("Hatalı değer Girdiniz !")

        if(operator == "+"):
            print("İşleminizin Sonucu: " + str(toplama(s1,s2)))
        elif(operator == "-"):
            print("İşleminizin Sonucu: " + str(cikarma(s1,s2)))
        elif(operator == "*"):
            print("İşleminizin Sonucu: " + str(carpma(s1,s2)))
        elif(operator == "/"):
            print("İşleminizin Sonucu: " + str(bölme(s1,s2)))
        elif(operator == "%"):
            print("İşleminizin Sonucu: " + str(kalan(s1,s2)))
        else:
            print("Yanlış bir operator girdiniz")

        tercih = input("Başka bir işlem ? [E/H]")

        if(tercih == "H" or tercih == "h"):
            break;
main()
