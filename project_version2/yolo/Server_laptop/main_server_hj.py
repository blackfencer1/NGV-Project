import cv2
import numpy as np
import threading
import time
import FrameProcess
import server
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'python/'))
sys.path.append(os.getcwd().replace('darknet', ''))

imgcnt = 1


def main():
    ts = Telecommunication()
    while True:
        ts.recvframe()
        runYolo()
        time.sleep(4)
        ts.sendcoordinates()


def runYolo():
    global imgcnt
    # command: run yolo
    os.system(
        './darknet detector demo data/obj.data cfg/yolov3.cfg backup/yolov3_3300.weights '
        'camData/image%s.jpg' % imgcnt)
    imgcnt += 1


if __name__ == '__main__':
    print("### main start ###")
    main()
