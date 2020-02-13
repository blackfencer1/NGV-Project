import cv2
import numpy as np
import os

#색상 범위 - HSV - 색상(Hue), 채도(Saturation), 명도(Value)
lower_orange = (8, 50, 50)
upper_orange = (20, 255, 255)

color_white = (255, 255, 255)
####

# 20년02월14일 측정한 온도매핑 좌표 #
corner = [[255, 265],
          [210, 466],
          [530, 444],
          [436, 270]]    # 640X480 기준
####



# 주황색을 검출하기 위한 함수 #
def find_orange(img):
    # 가우시안55 필터 적용
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 색상 범위를 제한하여 mask 생성
    img_mask = cv2.inRange(img_hsv, lower_orange, upper_orange)

    # 원본 이미지를 가지고 Object 추출 이미지로 생성
    img_result = cv2.bitwise_and(img, img, mask=img_mask)

    return img_result

# 주황색을 검출하기 위한 함수 #
def find_white(img):
    # 가우시안55 필터 적용
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 색상 범위를 제한하여 mask 생성
    img_mask = cv2.inRange(img_hsv, (0, 0, 100), (255, 250, 255))

    # 원본 이미지를 가지고 Object 추출 이미지로 생성
    img_result = cv2.bitwise_and(img, img, mask=img_mask)

    return img_result

def make_box(img, center_x, center_y, width, height):
    '''
    이미지에 색깔있는 박스를 만들어주는 함수
    :param img: 배경 이미지
    :param center_x: 박스의 x좌표
    :param center_y: 박스의 y좌표
    :param width: 박스의 크기
    :param height: 박스의 크기
    :return: 박스 합성이 된 이미지
    '''
    # ROI 영역
    vertices = np.array(
        [[(center_x - width / 2, center_y - height / 2),
          (center_x - width / 2, center_y + height / 2),
          (center_x + width / 2, center_y + height / 2),
          (center_x + width / 2, center_y - height / 2)]],
        dtype=np.int32)
    cv2.fillPoly(img, vertices, (0, 0, 255))

    return img


def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global points
        points.append([x, y])
        print(points)

def image_het(image, corner):
    '''
    이미지를 네개의 모서리에 맞춰서
    형태를 변환해주는 함수
    :param image: 변환할 이미지
    :param corner: 형태를 변환할 네개의 모서리
    :return: 변환된 이미지
    '''

    points = list()
    cv2.setMouseCallback('box', on_mouse)

    h, w = image.shape[:2]
    print(w)
    print(h)
    rows, cols, ch = image.shape

    pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    pts2 = np.float32([corner[0], corner[3], corner[1], corner[2]])

    M = cv2.getPerspectiveTransform(pts1, pts2)

    dst = cv2.warpPerspective(img, M, (cols, rows))

    image_result = dst
    return image_result

if __name__ == '__main__':
    print("##### clibration start #####")

    # 파일리스트 읽어오기
    path_read = './het_calibration_image'
    file_list_read = os.listdir(path_read)

    img = cv2.imread("het_calibration_image/" + file_list_read[10])  # 이미지 읽기

    # img = cv2.resize(img, (800, 480), interpolation=cv2.INTER_CUBIC)
    #img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #img_orange = find_white(img)

    # 온도센서 모서리 좌표
    corner_1 = [255, 265]
    corner_2 = [210, 466]
    corner_3 = [530, 444]
    corner_4 = [436, 270]

    ### box 생성 ###
    img_box = make_box(img, corner_1[0], corner_1[1], 4, 4)
    img_box = make_box(img_box, corner_2[0], corner_2[1], 4, 4)
    img_box = make_box(img_box, corner_3[0], corner_3[1], 4, 4)
    img_box = make_box(img_box, corner_4[0], corner_4[1], 4, 4)
    ################

    img_het = image_het(img, corner)

    #cv2.imshow('image', img)
    cv2.imshow('fsdfsdf', img_het)
    cv2.imshow('box', img_box)
    cv2.waitKey(0)

    print("#### clibration end ####")
