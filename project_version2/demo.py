'''
프로그램 내용 : 저장된 이미지와 온도데이터와 yolo좌표를
                한꺼번에 받아서 처리하기 위한 내용

                온도데이터는 카메라 이미지와 해상도가
                일치하도록 mapping이 되어있는 온도이미지를
                사용하여 처리
'''

import os
import cv2
import numpy as np
import ImagePreProcess as ipp

yolo_location = [4, 6, 4, 6]
# flat_het = [12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
#              12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
#              12, 12, 12, 12, 12, 0, 12, 12, 12, 12,
#              12, 12, 12, 12, 0, 0, 0, 0, 12, 12,
#              12, 12, 12, 12, 0, 0, -2, 0, 12, 12,
#              12, 12, 12, 12, 12, 0, 0, 0, 12, 12,
#              12, 12, 12, 12, 12, 0, 0, 12, 12, 12,
#              12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
#              12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
#              12, 12, 12, 12, 12, 12, 12, 12, 12, 12]

width = 10
height = 10

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
    blackice = np.zeros((width*height), dtype=np.int8)
    print(het[4], yolo[4])
    print(het[4].dtype, yolo[4].dtype)
    for index in range(len(het)):
        if (het[index] is 1) and (yolo[index] is 1):
            blackice[index] = 1
            print(blackice[index])
    print(blackice)
    return blackice

print("start")
flat_yolo = yolo_arr2flat(yolo_location)
het_image = cv2.imread("het_image.JPG", cv2.IMREAD_COLOR)
flat_het = image_het2flat(het_image)
flat_het = np.array(flat_het)
# print("flat het shaep : ", flat_het.shape)
print("start find black ice")
blackice = Find_BlackIce(flat_het, flat_yolo)
print("flat_het :", flat_het)
print("flat_yolo : ", flat_yolo)
for i in range(10):
    print(blackice[10*i], blackice[10*i+1], blackice[10*i+2], blackice[10*i+3], blackice[10*i+4],
          blackice[10*i+5], blackice[10*i+6], blackice[10*i+7], blackice[10*i+8], blackice[10*i+9])

