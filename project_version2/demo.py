'''
프로그램 내용 : 저장된 이미지와 온도데이터와 yolo좌표를
                한꺼번에 받아서 처리하기 위한 내용
'''

import os
import cv2
import numpy as np
import ImagePreProcess as ipp

yolo_location = [4, 6, 4, 6]
flat_het = [12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
             12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
             12, 12, 12, 12, 12, 0, 12, 12, 12, 12,
             12, 12, 12, 12, 0, 0, 0, 0, 12, 12,
             12, 12, 12, 12, 0, 0, -2, 0, 12, 12,
             12, 12, 12, 12, 12, 0, 0, 0, 12, 12,
             12, 12, 12, 12, 12, 0, 0, 12, 12, 12,
             12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
             12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
             12, 12, 12, 12, 12, 12, 12, 12, 12, 12]

width = 10
height = 10

def yolo_arr2flat(yolo_location):
    x = yolo_location[0] # 위에서 아래로 중심 높이
    y = yolo_location[1] # 왼쪽에서 오른쪽으로 중심 너비
    w = yolo_location[2]
    h = yolo_location[3]

    flat_yolo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(10):
        for j in range(10):
            if (i+1 >= x-h/2) and (i+1 <= x+h/2):
                if (j+1 >= y-w/2) and (j+1 <= y+w/2):
                    flat_yolo[i*width + j] = 1

    print("flat yolo : ", flat_yolo)
    return flat_yolo

def Find_BlackIce(het, yolo):
    blackice = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(len(het)):
        if (het[i] <= 0) and (yolo[i] is 1):
            blackice[i] = 1

    return blackice

print("start")
flat_yolo = yolo_arr2flat(yolo_location)
print("start find black ice")
blackice = Find_BlackIce(flat_het, flat_yolo)

for i in range(10):
    print(blackice[10*i], blackice[10*i+1], blackice[10*i+2], blackice[10*i+3], blackice[10*i+4],
          blackice[10*i+5], blackice[10*i+6], blackice[10*i+7], blackice[10*i+8], blackice[10*i+9])