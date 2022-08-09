__author="Emre Nihat Durgun"


def yaskontrol(yas):
    if(yas <100):
        if(yas <50):
            print("Yaşınız 0-50 Aralığındandır!")
        elif(yas > 50):
            print("Yaşınız 50-100 Aralığındandır!")
        elif(yas==50):
            print("Yaşınız 50'lidir.")
    elif(yas > 100):
        print("Lütfen 0-100 Arasında Bir Değer Giriniz")
    elif(yas == 100):
        print("Yaşınız 100'lidir.")
    else:
        print("Hatalı Bir Değer Girdiniz")


yas = int(input("Lütfen Yaşınızı Giriniz: "))
yaskontrol(yas)
