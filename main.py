"""
코드 작성일시 : 2020년 1
import cv2
import DataPreProcess as DPP
월 11일
작성자 : Park Jinsuk
코드 내용 : 전반적인 코드
"""
import cv2
import DataPreProcess as DPP

if __name__ == '__main__':
    print("this is main")

    # image = cv2.imread('test_image/1_cam-image_array_.jpg')  # 이미지 읽기
    # image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 입력 받은 화면 Gray로 변환
    # image1 = cv2.Canny(image1, threshold1 = 200, threshold2=300)
    # image1 = cv2.GaussianBlur(image1, (5, 5), 0)
    # cv2.imshow('orange', image1)
    # cv2.waitKey(0)

    # 학습시 필요한 이미지 전처리
    DPP.data_preprocess()