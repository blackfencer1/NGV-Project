#-*-coding: utf-8 -*-
"""
Date : 2020.02.08
Code : Rpi for display 
"""
import cv2
import socket
import numpy as np
import threading
import time
import ImagePreProcess as ipp

######## Global variables ########
# Lane Detection
frame = np.zeros(shape=(480, 640, 3), dtype="uint8")
frame_edge = np.zeros(shape=(480, 640, 3), dtype="uint8")
# Socket
frame_s = np.zeros(shape=(480, 640, 3), dtype="uint8")
array_location = []
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
'''
# Temperature
array_het = []
frame_het = np.zeros(shape=(480, 640,3), dtype="uint8")
'''

def main():
    global frame
    global frame_edge
    global frame_s
    global sock

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('172.20.10.11', 1234))
    print('connected')
    
    cam = cv2.VideoCapture(0)
    # sock.connect(('172.20.10.11', 1234))

    # Start threads
    myDetectLane = DetectLane()
    myDetectLane.start()
    mySockYolo = SockYolo()
    mySockYolo.start()
    '''
    myHetImage = GenerateHetImage()
    myHetImage.start()
    '''
    while True:
        ret, frame = cam.read()
        np.copyto(frame_s, frame)
        print("copy successfully")
        time.sleep(0.01)

        # frame_resize = cv2.resize(_frame, (800, 480), interpolation=cv2.INTER_CUBIC)
        cv2.imshow("frame", frame)
        cv2.imshow("frame_line", frame_edge)
        
        if cv2.waitKey(1) > 0:
            break

    cam.release()
    cv2.destroyAllWindows()


# Lane Detection Thread
class DetectLane(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = np.zeros(shape=(480, 640, 3), dtype="uint8")
        print("[Thread] Generate Image(DetectLane)")

    def run(self):
        global frame_edge
        global frame
        while True:
            self.frame = frame
            self.frame = ipp.filter_edge(self.frame)
            img_hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(img_hsv, np.array([0, 0, 100]), np.array([255, 255, 255]))
            frame_edge = cv2.bitwise_and(self.frame, self.frame, mask=mask)
            time.sleep(0.01)

    def shutdown(self):
        pass


# Socket Thread
class SockYolo(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame_s = np.zeros(shape=(480, 640, 3), dtype="uint8")
        self.data_s = None
        self.data_f = None
        self.stringData = None
        print("[Thread] Socket Communication")

    def run(self):
        global frame_s
        global sock
        while True:
            # Socket with Yolo
            self.frame_s = frame_s
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            result, self.frame_s = cv2.imencode('.jpg', self.frame_s, encode_param)
            self.data_s = np.array(self.frame_s)
            self.stringData = self.data_s.tostring()
            sock.sendall((str(len(self.stringData))).encode().ljust(16) + self.stringData)
            time.sleep(0.1)
            # Socket with html
            self.data_f = sock.recv(64)
            print(self.data_f)
            time.sleep(0.1)

    def shutdown(self):
        pass

'''
# HetImage Generation Thread
class GenerateHetImage(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame_het = np.zeros(shape=(480, 640, 3), dtype="uint8")
        print("[Thread] Generate Image(Het)")

    def run(self):
        global array_het
        global frame_het
        while True:
            frame_het = ipp.het_arr2img(array_het)
            time.sleep(0.01)

    def shutdown(self):
        pass
'''
if __name__ == '__main__':
    print("### main start ###")
    main()


