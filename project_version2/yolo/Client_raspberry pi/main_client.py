import cv2
import numpy as np
import threading
import time
import FrameProcess
import dataserver
import sys
import os
from os.path import isfile, join
sys.path.append(os.path.join(os.getcwd(), 'python/'))
sys.path.append(os.getcwd().replace('darknet', ''))
# sys.path.append(os.getcwd().replace('darknet', 'camData/'))
# sys.path.append(os.getcwd().replace('darknet', 'img1/'))


class MainThread:
    def __init__(self):
        self.ts = Telecommunication()
        self.ts.streaming()
        self.ts.streaming.after(1000, FrameProcess.frame2video())
        FrameProcess.frame2video.after(3000, self.runYolo())
        self.runYolo().after(3000, self.ts.sendcoordinates())

    def runYolo(self):
        # command: run yolo
        os.system(
            './darknet detector demo data/obj.data cfg/yolov3.cfg backup/yolov3_3300.weights '
            'data/media/video{},avi'.format(video_name_cnt))
        print("Now Detecting Black Ice...")


MainThread()





def frame2video():
    pathIn = './camData/'
    fps = 0.5
    frame_array = []

    # video name count
    global video_name_cnt
    pathOut = './data/media/video{}.avi'.format(video_name_cnt)

    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]

    # for sorting the file names properly
    files.sort(key=lambda x: x[5:-4])
    files.sort()
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]

    # for sorting the file names properly
    files.sort(key=lambda x: x[5:-4])
    for i in range(len(files)):
        filename = pathIn + files[i]

        # reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)

        # inserting the frames into an image array
        frame_array.append(img)

    out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()
    print('Make video{} successfully!'.format(video_name_cnt))


video_name_cnt += 1
print("video Number: ", video_name_cnt)
frame2video()