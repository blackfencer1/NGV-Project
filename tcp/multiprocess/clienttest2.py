import socket
import cv2
import socket
import numpy as np

if __name__ == "__main__":
	
	# create TCP Socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# server IP, port
	s.connect(("localhost", 5000))
	print('c1 connected')


    # webcam image capture
    cam = cv2.VideoCapture(0)

    # change image properties (3 = width, 4 = height)
    cam.set(3, 320);
    cam.set(4, 240);

    ## 90 image between 0 to 100 (default = 95)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    # read viedo per 1 frame
	# success: ret = True, fail: ret = False, frame: read frame
    ret, frame = cam.read()
    # cv2. imencode(ext, img [, params])
	# encoding image frame to jpg(form: encode_param)
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    # tranform frame to String
    data = numpy.array(frame)
    stringData = data.tostring()

    # transform data to server
    #(str(len(stringData))).encode().ljust(16)
    s.sendall((str(len(stringData))).encode().ljust(16) + stringData)

cam.release()

