"""
코드 작성일시 : 2020년 1월 11일
작성자 : Park Jinsuk
코드 내용 : 특정색깔을 검출하기 위한 함수들을 작성

수정 날짜 : 2020년 1월 12일
           추가 = 머신러닝을 위한 이미지 전처리 함수 작성
"""

import cv2
import os

# 색상 범위 - HSV - 색상(Hue), 채도(Saturation), 명도(Value)
# 원본
# lower_orange = (8, 50, 50)
# upper_orange = (20, 255, 255)
#
# lower_white = (0, 0, 210)
# upper_white = (255, 255, 255)

# 테스트값
lower_orange = (8, 50, 50)
upper_orange = (20, 255, 255)

lower_white = (0, 0, 200)
upper_white = (255, 100, 255)




# 차선의 주황색을 검출하기 위한 함수 #
def find_line_orange(img):
    # 가우시안55 필터 적용
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 색상 범위를 제한하여 mask 생성
    img_mask = cv2.inRange(img_hsv, lower_orange, upper_orange)

    # 원본 이미지를 가지고 Object 추출 이미지로 생성
    img_result = cv2.bitwise_and(img, img, mask=img_mask)

    return img_result


# 차선의 하얀색을 검출하기 위한 함수 #
def find_line_white(img):
    #가우시안55, bilateral 필터적용
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.bilateralFilter(img, 15, 75, 75)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 색상 범위를 제한하여 mask 생성
    img_mask = cv2.inRange(img_hsv, lower_white, upper_white)

    # 원본 이미지를 가지고 Object 추출 이미지로 생성
    img_result = cv2.bitwise_and(img, img, mask=img_mask)

    return img_result


# 차선들의 이미지를 합치고 하늘배경을 제거하는 함수 #
# img1, img2 인자는 합성할 이미지
# pixel 은 이미지 위에서부터 제거할 픽셀수
def merge_lines(img1, img2, pixel):

    for i in range(70):
        for j in range(160):
            #print(img1[i, j])
            img1[i+50, j] = [0, 0, 255]

    img_result = cv2.bitwise_or(img1, img2)

    for i in range(pixel):
        for j in range(160):
            img_result[i, j] = [0, 0, 0]  # 검은색으로 채움

    return img_result

def filter_edge(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 입력 받은 화면 Gray로 변환
    img = cv2.Canny(img, threshold1 = 200, threshold2=300)
    img = cv2.GaussianBlur(img, (5, 5), 0)

    for i in range(50):
        for j in range(160):
            img[i, j] = 0  # 검은색으로 채움
    return img

def filter_color(img):
    line_orange = find_line_orange(img)

def data_preprocess():
    path_read = './test_image'
    path_write = './train_image'

    # 파일리스트 읽어오기
    file_list_read = os.listdir(path_read)
    file_list_write = os.listdir(path_write)
    # 저장할 디덱토리 비어있지 않을 경우 예외처리
    if (len(file_list_write) != 0):
        print("데이터를 저장할 디렉토리가 비어있지 않습니다.")
        return 0

    for i in range(len(file_list_read)):
        image = cv2.imread("test_image/"+file_list_read[i])  # 이미지 읽기


        # 이미지 전처리 과정
        image = filter_color(image)
        #image = filter_edge(image)

        # 이미지 저장
        # cv2.imwrite("train_image/"+file_list_read[i], line_image)

        # 변환 중인 이미지 보여줌
        cv2.imshow('a', image)
        cv2.waitKey(50)

        # 변환 진행과정 표시
        print("{} of {} : {}".format(i+1, len(file_list_read)+1, file_list_read[i]))

    print("Preprocessing Complete!")
