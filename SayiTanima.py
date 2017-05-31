import sys
ayrac = "##############################################"
x = 0
kontrol = True
def main(): 
 global x,kontrol
 print ("Hoşgeldiniz ! :)")
 while(True):
   kontrol = True
   print (ayrac)
   try:
       x = input("Bir sayı giriniz: ")
       x = int(float(x))
       islemler()
   except ValueError :
       print("Geçersiz değer girdiniz !")
       kontrol = False
   while(kontrol):
    durum = input("Devam etmek istiyor musunuz (E / H): ")
    if(durum[0] ==   "H" or durum[0] == "h"):
        print("Program Kapatılıyor !")
        print (ayrac)
        kontrol =True
        sys.exit(0)
    elif (durum[0] == "E" or durum[0] == "e"):
        print("Devam etmeyi seçtiniz !")
        kontrol = False
    else:
        print("Geçersiz değer girdiniz !")
        kontrol = True
        print (ayrac)

def islemler():
 global x
 if(x < 0):
  print(str(x) +" Bu sayı negatiftir.")
  print (ayrac)
 elif (x > 0):
  print(str(x) +" Bu sayı pozitiftir.")
  print (ayrac)
 else:
  print("Bu sayı 0'dır.")
  print (ayrac)

main()
