from twilio.rest import Client as TwilioRestClient
from urllib.request import urlopen
import urllib
import time
from datetime import date 

ftime = True
status = True 
account_sid = "ACc2478e661662daf28b8346a9f633747f"
auth_token = "2a6ab44306cdbffd6888c0748782bcc9"
client = TwilioRestClient(account_sid, auth_token)
msg = []
count = 0

def send_sms(text):
    message = client.messages.create(to="+15183191368", from_="+14844699351",body=text)

def read_sms():
    for message in client.messages.list():
        print(message.body)

def sms_notify():
    global ftime
    d = date.fromordinal(730920)
    today = d.strftime("(%d,%m,%y)")
    count = 0
    for message in client.messages.list( from_="+15183191368",
    date_sent=today ):
            count += 1
    while status:
        text = []
        for message in client.messages.list( from_="+15183191368",
    date_sent=today ):
            text += [message.body]
        lastext = text[0]
        split = lastext.split()
        if (count < len(text) ):
            count = len(text)
            print("Machine have new message: "+lastext)
            return lastext
        if ftime == True:
            ftime =False
            print("Sms notify service is opening...")

def open_service():
    global msg
    print("\nSms service is opening...")
    for message in client.messages.list():
        msg += [message]
    sms_notify()

def remove_sms(message_sid):
    
    client.messages.redact(message_sid)
    message = client.messages.get(message_sid)

    client.messages.delete(message_sid)
    
def auto_sms():
    text = ["hi admin","how are you","what is your name","1","2","3","4","5"]
    for m in text:
        send_sms(m)
        time.sleep(45)


def close_service():
    global status
    status = False
    print("Sms notify service is closing")
    print("Sms service is closing")
