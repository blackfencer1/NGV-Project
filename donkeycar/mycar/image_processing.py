'''
영상처리만을 위한 스레드
'''

import threading
import cv2
import numpy as np
import os
import time
import display


class image_process(threading.Thread):
    def __init__(self, tub_class_name):
        print("### image_process thread __init__ ###")
        threading.Thread.__init__(self)
        threading.Thread.name = "thread_image_process"
        self.tub_class_name = tub_class_name
        self.frame = np.zeros((480, 800, 3), dtype=np.uint8)

    def run(self):
        print("### image_process thread run ###")
        while True:
            if self.frame is None:
                continue

            self.frame = display.filter_edge(self.frame)
            self.frame = cv2.resize(img, (800, 480), interpolation=cv2.INTER_CUBIC)

            img_hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(img_hsv, np.array([0, 0, 100]), np.array([255, 255, 255]))
            self.frame = cv2.bitwise_and(self.frame, self.frame, mask=mask)

            cv2.imshow("test", self.frame)
            cv2.waitKey(50)
            self.frame = None

    def shutdown(self):
        pass

if __name__ == '__main__':

    Image_Processing = image_process(TubWriter)
    Image_Processing.start()

    Image_Processing.frame = TubWriter.frame