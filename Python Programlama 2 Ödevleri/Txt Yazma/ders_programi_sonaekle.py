__author__="Emre Nihat Durgun"
import os

def txtekle():
    with open(os.getcwd()+"\\ders_programi.txt","a") as file:
        file.write("\nPython Programlama-2: 4 Modül 2 Saat")
    print("ders_programi.txt dosyasına ekleme işlemi başarılı")

print("ders_programi.txt adlı dosyaya ekleme işlemi başladı")
print("Yazılacak Değer:\"Python Programlama-2: 4 Modül 2 Saat\" ")
txtekle()
