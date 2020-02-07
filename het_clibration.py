import cv2
import numpy as np
import os

# 파일리스트 읽어오기
path_read = './het_calibration_image'
file_list_read = os.listdir(path_read)

image = cv2.imread("het_calibration_image/" + file_list_read[0])  # 이미지 읽기

#img = cv2.resize(img, (800, 480), interpolation=cv2.INTER_CUBIC)
img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

cv2.imshow('image', image)
cv2.imshow('hsv', img_hsv)
cv2.waitKey(0)