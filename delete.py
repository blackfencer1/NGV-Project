import os, time
from firebase import firebase

firebase = firebase.FirebaseApplication("https://blackice-proj.firebaseio.com/", None)
result = firebase.get('/Detection',None)

while True:
    if result==True:
        print("detect O")
        os.system("mpg321 text.mp3")
        time.sleep(4)
    else:
        print("detect X")
