"""
코드 작성일시 : 2020년 2월 8월
코드 내용 : 디스플레이 해주는 라즈베리파이를 따로
            추가하면서 이미지 처리코드를 분리
"""
import os
import cv2
import numpy as np
import threading
import socket
import time
from queue import Queue
import ImagePreProcess as ipp


######## 전역변수 #########
frame           = np.zeros(shape=(480, 640, 3), dtype="uint8")
frame_edge      = np.zeros(shape=(480, 640, 3), dtype="uint8")
frame_display   = np.zeros(shape=(480, 800, 3), dtype="uint8")
array_het       = []
frame_het       = np.zeros(shape=(480, 640, 3), dtype="uint8")
location_yolo   = None

IMAGE_NO        = 0
IMAGE           = 1
IMAGE_DISPLAY   = 2

HOST = '192.168.0.107'
PORT = 9999

server_socket = None
image_queue = Queue()

###########################

def main():
    """
    BlackFencer System의 main
    전역변수 frame을 사용하여 usb카메라의 사진을 저장하고
    각종 스레드들을 생성, 실행한다.
    :return: Nothing
    """
    global frame
    global image_queue

    cam = cv2.VideoCapture(0)

    # Thread start
    myDetectLine = DetectLane()
    myDetectLine.start()
    myHetImage = GenerateHetImage()
    #myHetImage.start()
    myDisplay = GenerateDisplayImage()
    myDisplay.start()
    mySaveImage = SaveImage(IMAGE_NO)
    mySaveImage.start()

    while True:
        _, _frame = cam.read()
        frame = ipp.rotation_image(_frame, 180)

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)

        data = np.array(imgencode)
        stringData = data.tostring()

        image_queue.put(stringData)

        cv2.imshow("frame", frame)

        # 키누르면 main 종료
        if cv2.waitKey(1) > 0:
            break

    cam.release()
    cv2.destroyAllWindows()


# Lane Detecting Thread
class DetectLane(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = np.zeros(shape=(480, 640, 3), dtype="uint8")
        print("[Thread] Generate Image(DetectLane)")

    def run(self):
        while True:
            global frame_edge
            global frame
            self.frame = frame
            self.frame = ipp.filter_edge(self.frame)
            #self.frame = ipp.detect_lane(self.frame)
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
        print("[Thread] Generate Image(Het)")

    def run(self):
        while True:
            global array_het
            global frame_het
            frame_het = ipp.het_arr2img(array_het)
            time.sleep(0.01)

    def shutdown(self):
        pass


class GenerateDisplayImage(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame_display = np.zeros(shape=(480, 800, 3), dtype="uint8")
        print("[Thread] Generate Image(display)")

    def run(self):
        global frame_edge
        global frame_display
        global frame_het
        global location_yolo
        while True:
            #frame = ipp.merge_image_het(frame_edge, frame_het)
            frame = frame_edge #임시방편

            if location_yolo is None:
                pass
            else:
                frame = ipp.image_object(frame, location_yolo[0], location_yolo[1],
                                         location_yolo[2], location_yolo[3])

            self.frame_display = cv2.resize(frame, (800, 480), interpolation=cv2.INTER_CUBIC)

            cv2.imshow("Display", self.frame_display)
            cv2.waitKey(1)
            time.sleep(0.01)

    def shutdonw(self):
        pass


class ServerSendImage(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global server_socket
        global HOST
        global PORT
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print("[Thread] Server Start (sending image)")

    def run(self):
        global server_socket
        global image_queue
        while True:
            client_socket, addr = server_socket.accept()

            try:
                data = client_socket.recv(1024)

                if not data:
                    print('Disconnected by ' + addr[0], ':', addr[1])
                    break

                stringData = queue.get()
                client_socket.send(str(len(stringData)).ljust(16).encode())
                client_socket.send(stringData)

            except ConnectionResetError as e:

                print('Disconnected by ' + addr[0], ':', addr[1])
                break

            client_socket.close()

            pass


    def shutdown(self):
        pass

class SaveImage(threading.Thread):
    def __init__(self, option):
        threading.Thread.__init__(self)
        self.option = option
        if self.option is IMAGE_NO:
            print("[Thread] {}Save Image".format("Don't "))
        elif self.option is IMAGE:
            print("[Thread] Save Image{}".format(" Pure"))
        elif self.option is IMAGE_DISPLAY:
            print("[Thread] Save Image{}".format(" Display"))
        else:
            print("[Thread] Wrong option!")

    def run(self):
        global frame
        global frame_display
        while True:
            if self.option is IMAGE_NO:
                break
            elif self.option is IMAGE:
                pass
                #저장
            elif self.option is IMAGE_DISPLAY:
                pass
                #저장
            else:
                break
            time.sleep(0.1)

    def shutdown(self):
        pass

if __name__ == '__main__':
    print("### main start ###")
    main()
