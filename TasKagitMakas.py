import random;
secim = -1      #senin secim
com_choice = -1; #bilgisayar secim
you_can = 3;    #senin canın    
com_can = 3;    #bilgisayar can
level = 1;      #level
def com_zeka():
global com_choice;
if(level == 1): #level göre zorluk artıyor,zorluk mekanizması ise kullanıcının sectiği değeri yenecek değerin artırılması
com_choice = random.choice(["0","1","2"]);
elif(level == 2):
if(secim == 0):
com_choice =  random.choice(["0","1","1","2"]);
elif(secim == 1):
com_choice = random.choice(["0","1","2","2"]);
elif(secim == 2):
com_choice = random.choice(["0","0","1","2"]);
elif(level == 3):
if(secim == 0):
com_choice = random.choice(["0","1","1","1","2"]);
elif(secim == 1):
com_choice =  random.choice(["0","1","2","2","2"]);
elif(secim == 2):
com_choice = random.choice(["0","0","0","1","2"]);
print("Oyun başlıyor...\n");
while(True):
print("\n");
print("Player Can: " + str(you_can) +"\nComputer Can: "+str(com_can) + "\nLevel: " + str(level)); #bu satırda can vb bilgileri gösteriyoruz
secim = input("Tas = 0,Kagıt = 1 Makas = 2 \nSecimini Yap: "); #bu satırda  kullanıcıdan secim alıyoruz
com_zeka();
print("Bilgisayar Seçimi: " +str(com_choice))
#Tas = 0,Kagıt = 1 Makas = 2
if(you_can > 0 and com_can > 0 and level <=  3):
if(str(secim) == "0" and str(com_choice) == "0"): #buralarda hangi değer hangi değerle olursa ne olur tarzında kodlamayı yaptık
print("Berabere kaldı!");
elif(str(secim) == "0" and str(com_choice) == "1"):
print("Bilgisayar kazandı!");
you_can -= 1;
elif(str(secim) == "0" and str(com_choice) == "2"):
print("Sen Kazandın!");
com_can -= 1;
if(secim == "1" and com_choice == "1"):
print("Berabere kaldı!\n");
elif(secim == "1" and com_choice == "2"):
print("Bilgisayar kazandı!");
you_can -= 1;
elif(secim == "1" and com_choice == "0"):
print("Sen Kazandın!\n");
com_can -= 1;
if(secim == "2" and com_choice == "2"):
print("Berabere kaldı!\n");
elif(secim == "2" and com_choice == "0"):
print("Bilgisayar kazandı!");
you_can -= 1;
elif(secim == "2" and com_choice == "1"):
print("Sen Kazandın!");
com_can -= 1;
elif(you_can > 0 and com_can == 0): #level artırma mekanizması
level += 1;
you_can +=1;
com_can = 3;
elif(you_can == 0 and com_can > 0): #oyunun bittiğini ve kaybettiğini gösteren mekanizma
print("Game over!You Lost!\n");
break;
elif(level == 4): #oyunun bittiğini ve kazandığınıe gösteren mekanizma
print("Game over!You win!\nd")
break;
