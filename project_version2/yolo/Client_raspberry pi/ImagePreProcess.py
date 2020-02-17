#-*-coding: utf-8 -*-
import cv2
import numpy as np
import os
import time  # 시간 측정을 위한 라이브러
import threading

# 색
color_yolo = (150, 110, 250)
color_black = (0, 0, 0)
color_red = (0, 0, 255)
color_white = (255, 255, 255)

#색상 범위 - HSV - 색상(Hue), 채도(Saturation), 명도(Value)
lower_orange = (8, 50, 50)
upper_orange = (20, 255, 255)

lower_white = (0, 0, 150)
upper_white = (255, 120, 255)
###

# 20년02월14일 측정한 온도매핑 좌표 #
corner = [[255, 265],
          [210, 466],
          [530, 444],
          [436, 270]]    # 640X480 기준
####


# ROI 설정하는 함수 (ROI영역이 사각형이 아니더라도 가능함)
def region_of_interest(img, vertices, color3=(255, 255, 255), color1=255):  # ROI 셋팅
    mask = np.zeros_like(img)  # mask = img와 같은 크기의 빈 이미지

    if len(img.shape) > 2:  # Color 이미지(3채널)라면 :
        color = color3
    else:  # 흑백 이미지(1채널)라면 :
        color = color1

    # vertices에 정한 점들로 이뤄진 다각형부분(ROI 설정부분)을 color로 채움
    cv2.fillPoly(mask, vertices, color)

    # 이미지와 color로 채워진 ROI를 합침
    ROI_image = cv2.bitwise_and(img, mask)
    return ROI_image

# 차선검출을 위한 엣지 필터함수 (sobel수직성분을 검출함)
def filter_edge(img):
    height, width = img.shape[:2]  # 이미지 높이, 너비

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 입력 받은 화면 Gray로 변환
    height_cut = 10

    # ROI 영역
    vertices = np.array(
        [[(0, height),
          (0, height_cut),
          (width, height_cut),
          (width, height)]],
        dtype=np.int32)

    img = region_of_interest(img, vertices)  # ROI 설정

    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    img = cv2.convertScaleAbs(img)
    img = cv2.cvtColor(np.copy(img), cv2.COLOR_GRAY2BGR)
    img = cv2.cvtColor(np.copy(img), cv2.COLOR_RGB2HLS)

    return img

# 온도이미지를 도로상 좌표로 매핑시킨 이미지
def image_het_mapping(img_het, corner=[[255, 265],
          [210, 466],
          [530, 444],
          [436, 270]]):

    # 온도이미지 mask 생성
    h, w = img_het.shape[:2]
    rows = 480
    cols = 640

    pts1 = np.float32([[w, 0], [0, 0], [w, h], [0, h]]) # 좌우반전 추가
    pts2 = np.float32([corner[0], corner[3], corner[1], corner[2]])

    M = cv2.getPerspectiveTransform(pts1, pts2)
    img_mask = cv2.warpPerspective(img_het, M, (cols, rows))

    return img_mask



# 온도센서로부터 이미지를 받아서 특정좌표에 이미지 합성
def merge_image_het(img, img_het, _corner=[[53, 59],
          [30, 94],
          [128, 94],
          [110, 59]]):

    print("corner :", _corner)
    # 온도이미지 mask 생성
    h, w = img_het.shape[:2]
    rows, cols, ch = img.shape

    pts1 = np.float32([[w, 0], [0, 0], [w, h], [0, h]]) # 좌우반전 추가
    pts2 = np.float32([_corner[0], _corner[3], _corner[1], _corner[2]])

    M = cv2.getPerspectiveTransform(pts1, pts2)
    img_mask = cv2.warpPerspective(img_het, M, (cols, rows))

    img_result = cv2.add(img, img_mask)

    return img_result


# 온도데이터 배열을 이미지로 바꿔주는 함수
def het_arr2img(num_array):
    h, w = num_array.shape[:2]  # 배열의 너비, 높이
    img = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            if num_array[i, j] > 5:
                img[i, j] = color_black
            elif num_array[i, j] > 0:
                img[i, j] = (0, 0, 100)
            elif num_array[i, j] > -5:
                img[i, j] = (0, 0, 180)
            else:
                img[i, j] = (0, 0, 255)

    return img

# csv형식의 hetadata를 img로 바꿔주는 함수 ########################################
# hetadata의 csv는 한줄에 768, 즉 1frame이 할당되어 저장이 된다.
# 몇가지 문제점 센서에서 csv로 저장하는 과정에서 [t, t, t]같이 대괄호가 생성이 된다.
# 이때 발생하는 nan값을 앞뒤 온도값으로 대체
def csv2img(csv):
    csv[0] = csv[1]
    csv[767] = csv[766]

    img = np.zeros((32, 24, 3), dtype=np.uint8)
    for i in range(32):
        for j in range(24):
            img[i, j] = csv[i*24 + j]

    return img

# 한줄형태의 hetadata를 이차원 배열로 바꿔주는 함수 ###
def flat2arr(csv):
    arr = np.zeros((32, 24), dtype=np.int8)
    csv[0] = csv[1]
    csv[767] = csv[766]

    for i in range(32):
        for j in range(24):
            #arr[i, j] = csv[i * 24 + j]
            arr[i, j] = csv[i * 24 + j] - 25

    return arr

# yolo에서 받은 좌표와 물체크기를 이미지 합성
def image_object(img, center_x, center_y, width, height):
    # ROI 영역
    vertices = np.array(
        [[(center_x - width / 2, center_y - height / 2),
          (center_x - width / 2, center_y + height / 2),
          (center_x + width / 2, center_y + height / 2),
          (center_x + width / 2, center_y - height / 2)]],
        dtype=np.int32)
    cv2.fillPoly(img, vertices, color_red)

    return img

# 차선의 주황색을 검출하기 위한 함수 #
def find_line_orange(img):
    # 가우시안55 필터 적용
    #img = cv2.GaussianBlur(img, (5, 5), 0)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 색상 범위를 제한하여 mask 생성
    img_mask = cv2.inRange(img_hsv, lower_orange, upper_orange)

    # 원본 이미지를 가지고 Object 추출 이미지로 생성
    img_result = cv2.bitwise_and(img, img, mask=img_mask)

    return img_result


# 차선의 하얀색을 검출하기 위한 함수 #
def find_line_white(img):
    #가우시안55, bilateral 필터적용
    #img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.bilateralFilter(img, 15, 75, 75)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 색상 범위를 제한하여 mask 생성
    img_mask = cv2.inRange(img_hsv, lower_white, upper_white)

    # 원본 이미지를 가지고 Object 추출 이미지로 생성
    img_result = cv2.bitwise_and(img, img, mask=img_mask)

    return img_result


# 이미지 회전
def rotation_image(img, degree):
    height, width = img.shape[:2]

    if degree%360 is 0:
        return img
    else:
        matrix = cv2.getRotationMatrix2D((width / 2, height / 2), degree, 1)
        img = cv2.warpAffine(img, matrix, (width, height))
        return img


def yolo_arr2flat(yolo_location):
    '''
    yolo좌표(중심높이좌표, 중심너비좌표, 가로길이, 세로길이)
    를 받아서 한줄로 flat하게 만들어 주는 함수
    :param yolo_location: yolo로부터 받는 좌표
    :return: flat yolo데이터
    '''
    x = yolo_location[0] # 위에서 아래로 중심 높이
    y = yolo_location[1] # 왼쪽에서 오른쪽으로 중심 너비
    w = yolo_location[2]
    h = yolo_location[3]

    width = 640
    height = 480

    flat_yolo = np.zeros((width*height), dtype=np.int8)

    for i in range(10):
        for j in range(10):
            if (i+1 >= x-h/2) and (i+1 <= x+h/2):
                if (j+1 >= y-w/2) and (j+1 <= y+w/2):
                    flat_yolo[i*width + j] = 1

    return flat_yolo

def image_het2flat(image_het):
    '''
    카메라 이미지에 mapping이 된 온도이미지를
    한줄로 flat하게 만들어주는 함수
    :param image_het: mapping이 된 온도이미지
    :return: flat 온도데이터
    '''

    width = 640
    height = 480

    img_het = cv2.resize(image_het, (width, height), interpolation=cv2.INTER_CUBIC)
    result = np.zeros((width * height), dtype=np.int8)

    for i in range(height):
        for j in range(width):
            if img_het[i, j] is (255, 100, 100):
                result[i*width + j] = (1)
            elif img_het[i, j] is (255, 200, 200):
                result[i*width + j] = (1)
            elif img_het[i, j] is (255, 255, 255):
                result[i*width + j] = (1)
            else:
                result[i*width + j] = (0)

    return result


def Find_BlackIce(het, yolo):
    '''
    flat형식의 온도데이터(het), yolo좌표(yolo)의 데이터를
    인덱스를 비교해가면서 둘다 1일때, 블랙아이스 리스트의
    값을 0에서 1로 바꿔준다.
    :param het: flat 온도데이터
    :param yolo: flat yolo데이터
    :return: flat 블랙아이스
    '''

    width = 640
    height = 480

    blackice = np.zeros((width*height), dtype=np.int8)
    print(het[4], yolo[4])
    print(het[4].dtype, yolo[4].dtype)
    for index in range(len(het)):
        if (het[index] is 1) and (yolo[index] is 1):
            blackice[index] = 1
            print(blackice[index])
    print(blackice)
    return blackice


def image_blackice(list_blackice):
    result = cv2.zeros(shape=(480, 640, 3), dtype="uint8")
    width = 640
    height = 480

    for i in range(height):
        for j in range(width):
            if list_blackice[i*640+j] is 1:
                result[i, j] = color_black
            else:
                result[i, j] = (255, 255, 255)

    return result



def display():
    print("## function display start ##")

    # 파일리스트 읽어오기
    path_read = './test_image'
    file_list_read = os.listdir(path_read)
    process_time = time.time()  # 프로세스 진행시간 측정

    for i in range(4):
        for j in range(2):
            if j is 0:
                corner[i][j] = corner[i][j] * 5
            else:
                corner[i][j] = corner[i][j] * 4

    het_image = cv2.imread("het_image.JPG")

    for i in range(len(file_list_read)):
        one_process_time = time.time()  # 프로세스 하나 진행시간 측정

        image = cv2.imread("test_image/" + file_list_read[i])  # 이미지 읽기

        img = filter_edge(image)
        img = cv2.resize(img, (800, 480), interpolation=cv2.INTER_CUBIC)

        # 이미지 좀더 선명하게 처리 #######
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv, np.array([0, 0, 100]), np.array([255, 255, 255]))
        img_2 = cv2.bitwise_and(img, img, mask=mask)
        ###################################

        # 온도 이미지 합성
        img_het = image_het(img_2, het_image, corner)
        img_het_object = image_object(img_het, 300, 200, 100, 50)

        # cv2.imshow('그냥 이미지', img)
        cv2.imshow('het image', img_het_object)
        print("{}\tof\t{} : {}\ttime : {}".format(i + 1, len(file_list_read) + 1, file_list_read[i],
                                                round(time.time() - one_process_time, 4)))

        cv2.waitKey(50)

    print("process total time : {}".format(time.time() - process_time))  # 프로세스 진행시간 표시



if __name__ == '__main__':
    print("##### main start #####")

    display()

    print("#### main end ####")
