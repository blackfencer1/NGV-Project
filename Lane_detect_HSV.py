import cv2
import os
import numpy as np

# 색상 범위 - HSV - 색상(Hue), 채도(Saturation), 명도(Value)
lower_orange = (8, 50, 50)
upper_orange = (20, 255, 255)

lower_white = (0, 0, 210)
upper_white = (255, 255, 255)

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



# 차선의 주황색을 검출하기 위한 함수 #
def find_line_orange(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 색상 범위를 제한하여 mask 생성
    img_mask = cv2.inRange(img_hsv, lower_orange, upper_orange)

    # 원본 이미지를 가지고 Object 추출 이미지로 생성
    img_result = cv2.bitwise_and(img, img, mask=img_mask)

    return img_result


# 차선의 하얀색을 검출하기 위한 함수 #
def find_line_white(img):
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
    img_result = cv2.bitwise_or(img1, img2)

    for i in range(pixel):
        for j in range(160):
            img_result[i, j] = [0, 0, 0]  # 검은색으로 채움

    return img_result


path_read = './test_image'


 # 파일리스트 읽어오기
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

    line_orange = find_line_orange(roi_img)
    line_white = find_line_white(roi_img)
    line_image = merge_lines(line_orange, line_white, 50)

    cv2.imshow('result', line_image)  # 흰색 차선 추출 결과 출력
    # cv2.imshow('result', image)  # 이미지 출력
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

    line_orange = find_line_orange(roi_img)
    line_white = find_line_white(roi_img)
    line_image = merge_lines(line_orange, line_white, 50)

    cv2.imshow('results',line_image) # 이미지 출력
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release
cap.release()
cv2.destroyAllWindows()
"""