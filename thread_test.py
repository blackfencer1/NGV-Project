"""
코드 작성일시 : 2020년 2월 2일
코드 내용 : 스레드 테스트 코드
"""
import threading
import cv2
import numpy as np
import os
import time
import display

from random import *


class data_send(threading.Thread):
    def __init__(self):
        self.isData = False
        print("### data_send thread __init__ ###")
        threading.Thread.__init__(self)
        threading.Thread.name = "thread_data_send"

    def run(self):
        print("### data_send thread run ###")
        while True:
            number_random = randint(1, 100)
            if number_random < 20:
                self.isData = True

                self.location_x = randint(300, 500)
                self.location_y = randint(100, 300)
                self.scale_w = randint(50, 100)
                self.scale_h = randint(50, 100)

            else:
                time.sleep(0.01)
                self.isData = False

    def shutdonw(self):
        pass


class data_receive(threading.Thread):

    def __init__(self, send_data_class):
        print("### data_receive thread __init__ ###")
        threading.Thread.__init__(self)
        threading.Thread.name = "thread_data_receive"
        self.send_data = send_data_class

    def run(self):
        print("### data_receive thread run ###")
        while True:
            if self.send_data.isData is True:
                self.location_x = self.send_data.location_x
                self.location_y = self.send_data.location_y
                self.scale_w = self.send_data.scale_w
                self.scale_h = self.send_data.scale_w
                time.sleep(0.01)
            else:
                time.sleep(0.01)
                pass

    def shutdown(self):
        pass


class image_processing(threading.Thread):
    def __init__(self):
        print("### image_process thread __init__ ###")
        threading.Thread.__init__(self)
        threading.Thread.name = "thread_image_process"
        self.frame = np.zeros((480, 800, 3), dtype=np.uint8)

    def run(self):
        print("### image_process thread run ###")
        while True:
            if self.frame is None:
                continue

            cv2.imshow("test", self.frame)
            cv2.waitKey(100)
            self.frame = None

    def shutdown(self):
        pass


if __name__ == '__main__':

    Thread_DataSend = data_send()
    Thread_DataReceive = data_receive(Thread_DataSend)

    Thread_DataSend.start()
    Thread_DataReceive.start()

    # 파일리스트 읽어오기
    path_read = './test_image'
    file_list_read = os.listdir(path_read)
    process_time = time.time()  # 프로세스 진행시간 측정

    for i in range(len(file_list_read)):
        image = cv2.imread("test_image/" + file_list_read[i])  # 이미지 읽기

        img = display.filter_edge(image)
        img = cv2.resize(img, (800, 480), interpolation=cv2.INTER_CUBIC)

        # 이미지 좀더 선명하게 처리 #######
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv, np.array([0, 0, 100]), np.array([255, 255, 255]))
        img_2 = cv2.bitwise_and(img, img, mask=mask)
        ###################################

        if Thread_DataSend.isData is True:
            img_2 = display.image_object(img_2, Thread_DataReceive.location_x,
                                         Thread_DataReceive.location_y,
                                         Thread_DataReceive.scale_w,
                                         Thread_DataReceive.scale_h)
        else:
            pass

        cv2.imshow("frame", img_2)
        cv2.waitKey(50)
