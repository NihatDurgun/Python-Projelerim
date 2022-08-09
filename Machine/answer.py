que_text = ["open face","stop face","what is your name"]

def makeanswer(text):
 if len(text) > 0:
    if que_text[0] == text:
        return "face.face_detect(True)","Face detection is opening",True #stringcode,Code olup olmadığı
    elif que_text[1] == text:
        return "face.face_detect(False)","Face detection is closing",True
    elif que_text[2] == text:
        return "Null","My name is machine !",False
    elif "#" == text[0]:
        return text[1:],"Code is starting",True
    else:
        return "Null","Null",False
