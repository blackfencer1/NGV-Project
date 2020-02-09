"""
코드 작성일시 : 2020년 2월 8월
코드 내용 : 디스플레이 해주는 라즈베리파이를 따로
            추가하면서 이미지 처리코드를 분리
"""
import os
import cv2
import numpy as np
import threading
import time
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

###########################

def main():
    """
    BlackFencer System의 main
    전역변수 frame을 사용하여 usb카메라의 사진을 저장하고
    각종 스레드들을 생성, 실행한다.
    :return: Nothing
    """
    global frame

    cam = cv2.VideoCapture(1)

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
