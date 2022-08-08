# -*- coding: utf-8 -*-
def getExam(i):
    while(1):
        try:
            resStr = input(str(i)+".nolu puani giriniz:");
            res = int(resStr)
            if(res >= 0 and res <= 100):
                return res
            else:
                print("Hatalı giris yaptınız:");
                continue;
        except:
            print("Hatali giris yaptınız:");
            continue;

def calculateNote(note):
    if note >= 90:
        deger="AA"
    elif note >=80:
        deger="BA"
    elif note >=70:
        deger="BB"
    elif note >=60:
        deger="CC"
    elif note >=50:
        deger="DC"
    elif note >=40:
        deger="DD"
    else:
        deger="FF"
    print("Notunuz : ",note,"  Harf Notunuz : ",deger)


p1 = getExam(1);
p2 = getExam(2);
p3 = getExam(3);
p4 = getExam(4);
p5 = getExam(5);
p6 = getExam(6);

note =(p1 * 0.10)+(p2 * 0.10)+(p3*0.10)+(p4*0.10)+(p5*0.20)+(p6*0.40)
calculateNote(note);
