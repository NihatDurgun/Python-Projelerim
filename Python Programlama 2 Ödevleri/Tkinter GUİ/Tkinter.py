import tkinter as tk

arayuz = tk.Tk()
button = None
label = None
def guiolustur():
    global button,label
    label = tk.Label(text="Merhaba Grafik Arayüz")
    button = tk.Button(text="Çık",command=cikis)
    label.pack()
    button.pack()
    
def cikis():
    global button,label,arayuz
    label['text']="Hoşcakal Grafik Arayüz..."
    button['text']="Lütfen Bekleyin..."
    button['state']="disabled"
    arayuz.after(2000,arayuz.destroy)

guiolustur()
arayuz.protocol('WM_DELETE_WİNDOW', cikis)

arayuz.mainloop()
