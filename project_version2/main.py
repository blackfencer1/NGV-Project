"""
코드 작성일시 : 2020년 2월 8월
코드 내용 : 디스플레이 해주는 라즈베리파이를 따로
            추가하면서 이미지 처리코드를 분리
"""
import cv2
import numpy as np
import threading
import time
import ImagePreProcess as ipp


######## 전역변수 #########
frame = np.zeros(shape=(480, 640, 3), dtype="uint8")
frame_edge = np.zeros(shape=(480, 640, 3), dtype="uint8")
frame_display = np.zeros(shape=(480, 800, 3), dtype="uint8")
array_het = []
frame_het = np.zeros(shape=(480, 640, 3), dtype="uint8")
location_yolo = None


###########################

def main():
    global frame

    cam = cv2.VideoCapture(1)

    # Thread start
    myDetectLine = DetectLane()
    myDetectLine.start()
    myHetImage = GenerateHetImage()
    #myHetImage.start()
    myDisplay = GenerateDisplayImage()
    myDisplay.start()

    while True:
        _, frame = cam.read()

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

if __name__ == '__main__':
    print("### main start ###")
    main()
