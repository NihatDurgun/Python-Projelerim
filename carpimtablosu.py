print("####### Emre Durgun Tarafından Yapılmıştır ########")
def islem(sayi=0):
    for i in range (0,11):
        print(str(i) +" kere " + str(sayi)+": " + str(i * int(sayi)))
    print("Tablonuz Bitti!")

while(True):
    sayi = input("Carpım Tablosunu Görmek İstediğiniz Sayıyı Girin: ")
    islem(sayi)
    drm = str(input("Devam Etmek İstermisiniz !"))
    if( drm == "H" or drm == "h" ):
        break