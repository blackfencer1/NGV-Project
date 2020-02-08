"""
코드 작성일시 : 2020년 2월 8월
코드 내용 : 디스플레이 해주는 라즈베리파이를 따로
            추가하면서 이미지 처리코드를 분리
"""
import cv2
import numpy as np
import threading
from threading import Thread
import time
import ImagePreProcess as ipp
import socket

# 전역변수
frame = np.zeros(shape=(480, 640, 3), dtype="uint8")
frame_edge = np.zeros(shape=(480, 640, 3), dtype="uint8")
frame_s = np.zeros(shape=(480, 640, 3), dtype="uint8")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.0.116', 8888))


def main():
    global frame
    global frame_edge
    global frame_s

    cam = cv2.VideoCapture(1)
    myDetectLane = DetectLane()
    mySockYolo = SockYolo()

    ret, frame = cam.read()
    time.sleep(1)
    myDetectLane.start()
    mySockYolo.start()

    while True:
        ret, frame = cam.read()
        frame_s.copyTo(frame)

        #frame_resize = cv2.resize(_frame, (800, 480), interpolation=cv2.INTER_CUBIC)
        cv2.imshow("frame", frame)
        cv2.imshow("frame_line", frame_edge)

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
            img_hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(img_hsv, np.array([0, 0, 100]), np.array([255, 255, 255]))
            frame_edge = cv2.bitwise_and(self.frame, self.frame, mask=mask)
            time.sleep(0.01)

    def shutdown(self):
        pass


class SockYolo(threading.Thread):
    import cv2
    import socket

    def __init__(self):
        threading.Thread.__init__(self)
        # self.frame = frame_s

    def run(self):
        global frame_s
        global sock
        while True:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            result, frame_s = cv2.imencode('.jpg', frame_s, encode_param)
            data = np.array(frame_s)
            stringData = data.tostring()
            sock.sendall((str(len(stringData))).encode().ljust(16) + stringData)


if __name__ == '__main__':
    print("### main start ###")
    main()

