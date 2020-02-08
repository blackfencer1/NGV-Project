"""
코드 작성일시 : 2020년 2월 8월
코드 내용 : 디스플레이 해주는 라즈베리파이를 따로
            추가하면서 이미지 처리코드를 분리
"""
import cv2
import numpy as np
import threading
import time
import imagepreprocess as ipp

# 전역변수
frame = np.zeros(shape=(480, 640, 3), dtype="uint8")
frame_edge = np.zeros(shape=(480, 640, 3), dtype="uint8")

def main():
    global frame
    global frame_edge

    Cam = cv2.VideoCapture(1)
    Detect_Line = detect_line()

    _, frame = Cam.read()
    time.sleep(1)
    Detect_Line.start()

    while True:
        _, frame = Cam.read()

        # frame_resize = cv2.resize(_frame, (800, 480), interpolation=cv2.INTER_CUBIC)
        cv2.imshow("frame", frame)
        cv2.imshow("frame_line", frame_edge)

        # 키누르면 main 종료
        if cv2.waitKey(1) > 0:
            break

    Cam.release()
    cv2.destroyAllWindows()


# 라인검출 스레드
class detect_line(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = np.zeros(shape=(480, 640, 3), dtype="uint8")

    def run(self):

        while True:
            global frame_edge
            self.frame = get_frame()
            self.frame = ipp.filter_edge(self.frame)
            img_hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(img_hsv, np.array([0, 0, 100]), np.array([255, 255, 255]))
            frame_edge = cv2.bitwise_and(self.frame, self.frame, mask=mask)

            #write_frame_edge(_frame_edge)
            time.sleep(0.01)

    def shutdown(self):
        pass


def get_frame():
    global frame
    return frame


def write_frame(_frame):
    global frame
    frame = _frame


def get_frame_edge():
    global frame_edge
    return frame_edge


def write_frame_edge(_frame):
    global frame_edge
    frame_edge = _frame


if __name__ == '__main__':
    print("### main start ###")
    main()
