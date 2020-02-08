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
frame       = None
frame_edge  = None

def main():
    Cam = cv2.VideoCapture(1)
    Detect_Line = detect_line()

    _, frame = Cam.read()

    Detect_Line.start()

    while True:
        _, frame = Cam.read()

        #frame_resize = cv2.resize(_frame, (800, 480), interpolation=cv2.INTER_CUBIC)
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
        self.frame = frame
        self.frame_edge = frame_edge

    def run(self):
        while True:
            self.frame = frame
            self.frame = ipp.filter_edge(self.frame)
            img_hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(img_hsv, np.array([0, 0, 100]), np.array([255, 255, 255]))
            self.frame_edge = cv2.bitwise_and(self.frame, self.frame, mask=mask)
            frame_edge = self.frame_edge
            time.sleep(0.001)

    def shutdown(self):
        pass


if __name__ == '__main__':
    print("### main start ###")
    main()
