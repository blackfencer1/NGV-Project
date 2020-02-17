'''
2020.02.13. - add socket
2020.02.15. - rpi: Server /laptop(yolo): Client
'''
import os
import cv2
import numpy as np
import threading
import socket
import time
import ImagePreProcess as ipp
from serial import Serial
import seeed_python_ircamera as ir


######## 전역변수 #########
frame = np.zeros(shape=(480, 640, 3), dtype="uint8")
frame_edge = np.zeros(shape=(480, 640, 3), dtype="uint8")
frame_display = np.zeros(shape=(480, 800, 3), dtype="uint8")
array_het = np.ones(shape=(32, 24, 1), dtype="int8")
frame_het = np.zeros(shape=(480, 640, 3), dtype="uint8")
location_yolo = [0]

IMAGE_NO = 0
IMAGE = 1
IMAGE_DISPLAY = 2
IMAGE_HET = 3

HET_NO = 0
HET = 1


###########################

# 온도센서
hetaData = np.ones((768,), dtype="int8")
lock = threading.Lock()
minHue = 180
maxHue = 360


def main():
    """
    BlackFencer System의 main
    전역변수 frame을 사용하여 usb카메라의 사진을 저장하고
    각종 스레드들을 생성, 실행한다.
    :return: Nothing
    """
    global frame
    global hetaData

    cam = cv2.VideoCapture(0)

    # Thread start
    myDetectLine = DetectLane()
    myDetectLine.start()
    myHetImage = GenerateHetImage()
    myHetImage.start()

    mySaveImage = SaveImage(IMAGE_NO, HET_NO)

    myDetectFrame = DetectFrame()
    myDetectFrame.start()

    myDisplay = GenerateDisplayImage()
    myDisplay.start()

    # IR CAMERA
    #app = ir.QApplication()
    dataThread = ir.DataReader(None)
    dataThread.start()

    # CAMERA
    _, frame = cam.read()
    mySaveImage.start()
    while True:
        _, frame = cam.read()

        #frame = ipp.rotation_image(_frame, 180)
        time.sleep(0.05)

    cam.release()
    cv2.destroyAllWindows()


# Lane Detecting Thread
class DetectLane(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = np.zeros(shape=(480, 640, 3), dtype="uint8")
        print("[Thread] Generate Image(Detect Lane)")

    def run(self):
        while True:
            global frame_edge
            global frame
            self.frame = frame
            self.frame = ipp.filter_edge(self.frame)
            # self.frame = ipp.detect_lane(self.frame)
            img_hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(img_hsv, np.array([0, 0, 100]), np.array([255, 255, 255]))
            frame_edge = cv2.bitwise_and(self.frame, self.frame, mask=mask)
            time.sleep(0.01)

    def shutdown(self):
        pass


# HetImage Generation Thread
class GenerateHetImage(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame_het = np.zeros(shape=(480, 640, 3), dtype="uint8")
        time.sleep(5)
        print("[Thread] Generate Image(Het)")

    def run(self):
        while True:
            global hetaData
            global array_het
            global frame_het
            hetaData = ir.hetaData
            array_het = ipp.flat2arr(hetaData)
            _frame_het = ipp.het_arr2img(array_het)
            frame_het = ipp.image_het_mapping(_frame_het, ipp.corner)
            time.sleep(0.01)

    def shutdown(self):
        pass


# SAVE IMAGE
class SaveImage(threading.Thread):
    def __init__(self, option_image, option_het):
        threading.Thread.__init__(self)
        self.option_image = option_image
        self.option_het = option_het
        self.count = 0

        # CREATE DIRECTORY
        # Camera image
        if not (os.path.isdir("./cam_data")):
            os.makedirs(os.path.join("cam_data"))
        # Het image
        if not (os.path.isdir("./het_data")):
            os.makedirs(os.path.join("het_data"))

        # Coordinate
        if not (os.path.isdir("./coord_data")):
            os.makedirs(os.path.join("coord_data"))

        time.sleep(2)

        # Camera Image
        if self.option_image is IMAGE_NO:
            print("[Thread] {}Save Image".format("Don't "))
        elif self.option_image is IMAGE:
            print("[Thread] Save Image{}".format(" Pure"))
        elif self.option_image is IMAGE_DISPLAY:
            print("[Thread] Save Image{}".format(" Display"))
        else:
            print("[Thread] Wrong image option!")

        # Temperature Image
        if self.option_het is HET_NO:
            print("[Thread] {}Save HET".format("Don't "))
        elif self.option_het is HET:
            print("[Thread] Save HET")
        else:
            print("[Thread] Wrong het option!")

    def run(self):
        global frame
        global frame_display
        global frame_het
        global array_het

        while True:
            self.count += 1
            if self.option_image is IMAGE_NO:
                pass
            elif self.option_image is IMAGE:
                cv2.imwrite("./cam_data/image.jpg", frame)
                pass
                # 저장
            elif self.option_image is IMAGE_DISPLAY:
                cv2.imwrite("./cam_data/image.jpg", frame_display)
                pass
                # 저장
            elif self.option_image is IMAGE_HET:
                cv2.imwrite("./het_data/image{0:0>5}.jpg".format(self.count), frame_het)
                pass
                # 저장
            else:
                pass

            if self.option_het is HET_NO:
                pass
            elif self.option_het is HET:
                file = open("./het_data/het{0:0>5}.txt".format(self.count), 'w')
                file.write(str(array_het))
                file.close()

            time.sleep(0.1)

    def shutdown(self):
        pass


# TELECOMMUNICATION: DETECTION DATA
class DetectFrame(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # Input server IP
        self.host = "192.168.0.122"
        self.port = 4000
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.host, self.port))
        print("connected")

    def run(self):
        global location_yolo
        while True:
            # SEND FRAME TO YOLO
            f = open("./cam_data/image.jpg", 'rb')
            frame_data = f.read()
            print("Read file: cam_data...")
            if frame_data:
                self.server_socket.send(str(len(frame_data)).ljust(16).encode())
                self.server_socket.send(frame_data)
                print('Send camera image successfully!')

            else:
                print('No Image')


class RecvCoord(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # Input server IP
        self.host = "192.168.0.122"
        self.port = 4000
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.host, self.port))
        print("connected")

    def sock(self):
        global location_yolo
        # RECEIVE COORDINATES FROM YOLO
        coord_data = self.server_socket.recv(1024)
        location_yolo = coord_data
        print("coordinates Update!", coord_data)

        with open("./coord_data/coordinates.txt", 'w') as my_file:
            print("receiving coordinates...")
            my_file.write(str(coord_data))
            print("coord : ", str(coord_data))
            my_file.close()


# IMAGE FOR DISPLAY
class GenerateDisplayImage(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame_display = np.zeros(shape=(480, 800, 3), dtype="uint8")
        print("[Thread] Generate Image(display)")

    def run(self):
        global frame
        global frame_edge
        global frame_display
        global frame_het
        global location_yolo
        while True:
            # frame = ipp.merge_image_het(frame_edge, frame_het)
            _frame = frame_edge  # 임시방편

            if location_yolo[0] is 0:
                print("### Wet Road is not detected... ####")
                pass
            else:
                print("##### Wet Road is DETECTED! #####")
                _frame = ipp.image_object(_frame, location_yolo[0], location_yolo[1],
                                          location_yolo[2], location_yolo[3])

            _frame = cv2.add(frame_edge, frame_het)
            self.frame_display = cv2.resize(_frame, (800, 480), interpolation=cv2.INTER_CUBIC)

            #cv2.imshow("het", frame_het)
            cv2.imshow("Display", self.frame_display)
            #cv2.imshow("framegfg", frame)

            cv2.waitKey(5)

    def shutdown(self):
        pass


if __name__ == '__main__':
    print("### main start ###")
    main()