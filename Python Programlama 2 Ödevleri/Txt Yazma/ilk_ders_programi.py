__author__="Emre Nihat Durgun"

import os
def txtyazdir():
    with open(os.getcwd() + "\\ders_programi.txt","w") as file:
        file.write("Python Programlama-1: 3 Modül 1,5 Saat")
    print("ders_programi.txt dosyasına yazma işlemi başarılı")

if(os.path.isfile(os.getcwd() + "\\ders_programi.txt") == False):
    print("ders_programi.txt Adlı Dosya Oluşturulacak!")

print("ders_programi.txt adlı dosyaya yazma işlemi başladı")
print("Yazılacak Değer: Python Programlama-1: 3 Modül 1,5 Saat")
txtyazdir()
