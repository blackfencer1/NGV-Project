'''
2020.02.11.
raspberry pi to Yolo server: MAKE A VIDEO
'''
import cv2
import numpy as np
import os
from os.path import isfile, join

video_name_cnt = 0


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
        size = (width,height)
        
        # inserting the frames into an image array
        frame_array.append(img)
           
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()
    print('Make video{} successfully!'.format(video_name_cnt))
    
video_name_cnt += 1
print("video Number: ",video_name_cnt)
frame2video()

