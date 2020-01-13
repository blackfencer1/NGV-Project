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

    image = cv2.imread('test_image/1_cam-image_array_.jpg')  # 이미지 읽기
    # a = DPP.find_line_orange(image)
    # b = DPP.find_line_white(image)
    # c = DPP.merge_lines(a, b, 50)
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (5, 5), 0)
    result1 = DPP.filter_binary(image)
    result2 = DPP.filter_binary(image)

    cv2.imshow('a', result1)
    cv2.imshow('b', result2)
    # cv2.imshow('c', c)
    cv2.waitKey(0)

    # 학습시 필요한 이미지 전처리
    #DPP.data_preprocess()