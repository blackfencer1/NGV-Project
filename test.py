"""
코드 작성일시 : 2020년 1월 11일
코드 내용 : 각종 테스트를 위한 임시코드들
"""
import cv2
import DataPreProcess as DPP


cap = cv2.VideoCapture(0)

print('width :%d, height : %d' % (cap.get(3), cap.get(4)))

while(True):
    ret, frame = cap.read()    # Read 결과와 frame

    if(ret) :
        #image = cv2.cvtColor(frame,  cv2.COLOR_BGR2GRAY)    # 입력 받은 화면 Gray로 변환
        image = cv2.GaussianBlur(frame, (5, 5), 0)
        image = cv2.bilateralFilter(image, 15, 75, 75)
        #result1 = DPP.filter_binary(image)
        #result2 = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 5)
        cv2.imshow('binary', image)    # 컬러 화면 출력
        #cv2.imshow('binaryinv', result2)    # 컬러 화면 출력


        #cv2.imshow('frame_gray', gray)    # Gray 화면 출력
        if cv2.waitKey(1) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()