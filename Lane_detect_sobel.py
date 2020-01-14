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


def draw_lines(img, lines, color=[0, 0, 255], thickness=2):  # 선 그리기
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):  # 허프 변환
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)

    return line_img


def weighted_img(img, initial_img, α=1, β=1., λ=0.):  # 두 이미지 operlap 하기
    return cv2.addWeighted(initial_img, α, img, β, λ)

def filter_edge(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 입력 받은 화면 Gray로 변환
    # 이미지 전처리 과정
    # ROI 영역
    vertices = np.array(
        [[(0, height),
          (0, height / 2),
          (width, height / 2),
          (width, height)]],
        dtype=np.int32)
    img = region_of_interest(img, vertices)  # ROI 설정
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    img = cv2.convertScaleAbs(img)
    for i in range(50):
        for j in range(160):
            img[i, j] = 0  # 검은색으로 채움
    return img

# 파일리스트 읽어오기
path_read = './test_image'
file_list_read = os.listdir(path_read)

for i in range(len(file_list_read)):
    image = cv2.imread("test_image/"+file_list_read[i])  # 이미지 읽기
    height, width = image.shape[:2]  # 이미지 높이, 너비

    sobel_img=filter_edge(image)
    cv2.imshow('result', sobel_img)  # 결과 이미지 출력
    cv2.waitKey(100)


"""
# 동영상 읽어오기
cap = cv2.VideoCapture('test_image/solidWhiteRight.mp4') # 동영상 불러오기

while(cap.isOpened()):
    ret, image = cap.read()
    height, width = image.shape[:2] # 이미지 높이, 너비

    gray_img = grayscale(image)  # 흑백이미지로 변환

    blur_img = gaussian_blur(gray_img, 3)  # Blur 효과

    canny_img = canny(blur_img, 150, 210)  # Canny edge 알고리즘

    # ROI 영역
    vertices = np.array(
        [[(0, height),
          (0, height / 2),
          (width, height / 2),
          (width, height)]],
        dtype=np.int32)
    ROI_img = region_of_interest(canny_img, vertices)  # ROI 설정

    hough_img = hough_lines(ROI_img, 1, 1 * np.pi / 180, 30, 10, 20)  # 허프 변환

    # result = weighted_img(hough_img, image)  # 원본 이미지에 검출된 선 overlap
    cv2.imshow('result', hough_img)  # 결과 이미지 출력
    cv2.waitKey(100)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release
cap.release()
cv2.destroyAllWindows()
"""