import cv2  # opencv 사용
import numpy as np
import os


def grayscale(img):  # 흑백이미지로 변환
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def canny(img, low_threshold, high_threshold):  # Canny 알고리즘
    return cv2.Canny(img, low_threshold, high_threshold)


def gaussian_blur(img, kernel_size):  # 가우시안 필터
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

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


# 파일리스트 읽어오기
path_read = './test_image'
file_list_read = os.listdir(path_read)

for i in range(len(file_list_read)):
    image = cv2.imread("test_image/"+file_list_read[i])  # 이미지 읽기
    height, width = image.shape[:2]  # 이미지 높이, 너비


    # 이미지 전처리 과정
    # ROI 영역
    vertices = np.array(
        [[(0, height),
          (0, height / 2),
          (width, height / 2),
          (width, height)]],
        dtype=np.int32)
    roi_img = region_of_interest(image, vertices)  # vertices에 정한 점들 기준으로 ROI 이미지 생성

    gray_img = grayscale(roi_img)  # 흑백이미지로 변환

    blur_img = gaussian_blur(gray_img, 3)  # Blur 효과

    canny_img = canny(blur_img, 70, 210)  # Canny edge 알고리즘

    cv2.imshow('result', canny_img)  # Canny 이미지 출력
    cv2.waitKey(100)



"""
# 동영상 읽어오기
cap = cv2.VideoCapture('test_image/solidWhiteRight.mp4') # 동영상 불러오기

while(cap.isOpened()):
    ret, image = cap.read()
    height, width = image.shape[:2] # 이미지 높이, 너비

    # ROI 영역
    vertices = np.array(
        [[(0, height),
          (0, height / 2),
          (width, height / 2),
          (width, height)]],
        dtype=np.int32)
    roi_img = region_of_interest(image, vertices)  # vertices에 정한 점들 기준으로 ROI 이미지 생성

    gray_img = grayscale(roi_img)  # 흑백이미지로 변환

    blur_img = gaussian_blur(gray_img, 3)  # Blur 효과

    canny_img = canny(blur_img, 70, 210)  # Canny edge 알고리즘

    cv2.imshow('result', canny_img)  # Canny 이미지 출력
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release
cap.release()
cv2.destroyAllWindows()
"""