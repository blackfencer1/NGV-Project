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

def main():
    Cam = cv2.VideoCapture(1)

    while True:
        _, frame = Cam.read()
        _frame = ipp.

        frame_resize = cv2.resize(frame, (800, 480), interpolation=cv2.INTER_CUBIC)
        cv2.imshow("VideoFrame", frame_resize)


        # 키누르면 main 종료
        if cv2.waitKey(1) > 0:
            break

    capture.release()
    cv2.destroyAllWindows()

def ImagePreprocessing(img):
    img_edge = display.filter_edge(img)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, np.array([0, 0, 100]), np.array([255, 255, 255]))
    img_result = cv2.bitwise_and(img, img, mask=mask)

    return img_result


if __name__ == '__main__':
    print("### main start ###")
    main()