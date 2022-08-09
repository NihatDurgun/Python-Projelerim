import speech

que_text = ["open face","stop face","what is your name"]

def answer(text):
    if que_text[0] == text:
        speech.talk("Face detection is opening")
        return "face.face_detect(True)",True #stringcode,Code olup olmadığı
    elif que_text[1] == text:
        speech.talk("Face detection is closing")
        return "face.face_detect(False)",True
    elif que_text[2] == text:
        speech.talk("My name is machine")
        return "Null",False
    else:
        return "Null",False
#8dfaf7839d2cdaae0c66d0057a206d2d
