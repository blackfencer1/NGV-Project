# coding: utf8
import cv2
import socket
import numpy as np
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server IP, port
s.connect(('192.168.1.83', 8485))
 
 
# webcam image capture
cam = cv2.VideoCapture(0)
 
# change image properties (3 = width, 4 = height)
cam.set(3, 320);
cam.set(4, 240);
 
## image property:90 (0~100) (default = 95)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
 
while True:
    # read viedo per 1 frame
	# success: ret = True, fail: ret = False, frame: read frame
    ret, frame = cam.read()
    # cv2. imencode(ext, img [, params])
	# encoding frame to jpg (form: encode_param)
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    # transform frame to String 
    data = numpy.array(frame)
    stringData = data.tostring()
 
    # send data to server
    #(str(len(stringData))).encode().ljust(16)
    s.sendall((str(len(stringData))).encode().ljust(16) + stringData)
 
cam.release()

