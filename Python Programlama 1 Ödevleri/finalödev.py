__author__="Final Projesi"
while(True):
    print("Sabah (1)/Öğle (2)/Akşam (3)")
    secim = input("Şu An Hangi Zamandasınız: ")
    if(secim=="1"):
        print("Şu An Sabah")
    elif(secim=="2"):
        print("Şu An Öğlen")
    elif(secim=="3"):
        print("Şu An Gece")
    else:
        print("Hatalı Değer.Program Kapatılıyor...")
        break
