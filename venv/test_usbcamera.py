import cv2

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

capture2 = cv2.VideoCapture(1)
capture2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


while True:
    ret, frame = capture.read()
    ret, frame2 = capture2.read()

    cv2.imshow("VideoFrame", frame)
    cv2.imshow("VideoFrame2", frame2)
    if cv2.waitKey(1) > 0: break

capture.release()
cv2.destroyAllWindows()