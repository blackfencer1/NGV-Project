'''
코드 내용 :
# 라즈베리파이 디스플레이에 보여줄 영상처리
도로 검출을 위한 영상처리로는 GaussianBlur, Sobel(수직)를 사용하였습니다.
# 특정object검출(yolo)과 온도데이터에 대한 이미지를 차선이미지에 합성합니다.

[수정 - 2020년1월20일] - object검출(yolo) 좌표를 받아 이미지 합성해주는 함수추가
                        온도 이미지 합성해주는 함수추가
[수정 - 2020년1월27일] - 온도데이터 배열to이미지 함수추가
[수정 - 2020년1월28일] - 실제 센서에서 받은 hetadata csv 읽어오기
                        csv를 2차원numpy배열로 변환하는 함수추가
                        cvs를 바로 image로 변환하는 함수추가(값에 따라 색차이 변경 미작성)
'''

import cv2
import numpy as np
import os
import time  # 시간 측정을 위한 라이브러

# 색
color_yolo = (150, 110, 250)
color_black = (0, 0, 0)
color_red = (0, 0, 255)
color_white = (255, 255, 255)


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

    # ROI 영역
    vertices = np.array(
        [[(0, height),
          (0, 45),
          (width, 45),
          (width, height)]],
        dtype=np.int32)

    img = region_of_interest(img, vertices)  # ROI 설정

    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    img = cv2.convertScaleAbs(img)
    img = cv2.cvtColor(np.copy(img), cv2.COLOR_GRAY2BGR)
    img = cv2.cvtColor(np.copy(img), cv2.COLOR_RGB2HLS)

    return img


# 온도센서로부터 이미지를 받아서 특정좌표에 이미지 합성
def image_het(img, img_het, center_x, center_y):
    w = 80
    h = 80

    # ROI 영역
    vertices = np.array(
        [[(center_x - w / 2, center_y - h / 2),
          (center_x - w / 2, center_y + h / 2),
          (center_x + w / 2, center_y + h / 2),
          (center_x + w / 2, center_y - h / 2)]],
        dtype=np.int32)
    #cv2.fillPoly(img, vertices, (0, 0, 0)) # 주석을 풀면 도로이미지 위에 그대로 합성됨

    roi_het = img[center_y - int(h/2): center_y + int(h/2), center_x - int(w/2): center_x + int(w/2)]
    img_het = cv2.resize(img_het, (w, h), interpolation=cv2.INTER_CUBIC)
    _img_roi = cv2.add(img_het, roi_het)
    np.copyto(roi_het, _img_roi)

    return img

# 온도데이터 배열을 이미지로 바꿔주는 함수
def het_num2img(num_array):
    print(num_array[0, 0])
    print(num_array[0, 11])
    h, w = num_array.shape[:2]  # 배열의 너비, 높이
    img = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            print('num_array[', i, j, '] :', num_array[i, j])
            if num_array[i, j] > 10:
                img[i, j] = color_black
            elif num_array[i, j] > 5:
                img[i, j] = (100, 0, 0)
            elif num_array[i, j] > 0:
                img[i, j] = (200, 0, 0)
            elif num_array[i, j] > -5:
                img[i, j] = (255, 100, 100)
            elif num_array[i, j] > -10:
                img[i, j] = (255, 200, 200)
            else:
                img[i, j] = color_white
            print('num_array[', i, j, '] :', num_array[i, j])

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
    arr = np.zeros((32, 24), dtype=np.uint8)
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


def display():
    print("## function display start ##")

    # 파일리스트 읽어오기
    path_read = './test_image'
    file_list_read = os.listdir(path_read)
    process_time = time.time()  # 프로세스 진행시간 측정

    ## 임시방편 임의의 온도배열 생성 12x6 ###
    ## 온도 데이터배열에서 이미지 전환 테스트 코드
    # hetadata = np.zeros((80, 15), dtype=np.int8)
    # for i in range(80):
    #     for j in range(15):
    #         if i < 40:
    #             hetadata[i, j] = (20 - i)
    #         else:
    #             hetadata[i, j] = (i - 60)

    # hetadata = np.array([[-10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10],
    #                      [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10],
    #                      [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10],
    #                      [-5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5],
    #                      [-5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5],
    #                      [-5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5],
    #                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                      [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    #                      [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    #                      [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    #                      [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
    #                      [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
    #                      [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
    #                      [20, 20, 20, 20, 20, 16, 17, 18, 19, 20, 21, 0]])

    het_data = np.genfromtxt('test_hetadata/result1.csv', delimiter=',')
    #het_image = csv2img(het_csv[0, :])
    het_arr = flat2arr(het_data[0, :])
    het_image = het_num2img(het_arr)

    #het_image = cv2.resize(het_image, (300, 300), interpolation=cv2.INTER_CUBIC)
    #cv2.imshow('het data image', het_image)
    #cv2.waitKey(10)
    ############################################
    #het_image = cv2.imread("het_image.JPG")

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
        img_het = image_het(img_2, het_image, 300, 300)
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
