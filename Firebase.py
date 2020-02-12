import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
import threading

db_url = 'https://blackice-proj.firebaseio.com/'
cred = credentials.Certificate("/home/pi/blackice-proj-firebase-adminsdk-w3e0r-3b4f9ce7ea.json")
default_app = firebase_admin.initialize_app(cred, {'databaseURL':db_url})

ref=db.reference('Detection')

def firebase_run():
    ref.update({"isDetect": True})
    time.sleep(4)
    ref.update({"isDetect": False})
    threading.Timer(4,firebase_run).start()

def main():
    firebase_run()

main()