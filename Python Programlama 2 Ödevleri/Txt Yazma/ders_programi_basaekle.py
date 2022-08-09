__author__="Emre Nihat Durgun"
import os

def txtekle():
    with open(os.getcwd()+"\\ders_programi.txt","r+") as file:
        file.read()
        file.seek(0)
        file.write("Python Programlama: 2 Ders 3,5 Saat\n")
    print("ders_programi.txt dosyasına başa ekleme işlemi başarılı")

print("ders_programi.txt adlı dosyaya başa ekleme işlemi başladı")
print("Yazılacak Değer:\"Python Programlama: 2 Ders 3,5 Saat\" ")
txtekle()

