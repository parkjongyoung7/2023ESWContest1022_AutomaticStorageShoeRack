import cv2
import numpy as np
import os

def shapeCheck(reference_contour, contour, shape_threshold):
    match = cv2.matchShapes(reference_contour, contour, cv2.CONTOURS_MATCH_I3, 0.0)
    if match < shape_threshold:
        return True
    else:
        return False


def shoe_detect_nums(image_path):
    # 변수 설정
    min_area = 200  
    max_area = 300
    shape_threshold = 0.42  # 모양 일치 정도의 임계값, 커질수록 널널하게
    count = 0

    # detection할 이미지 불러옴
    print(image_path)
    image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # 색 범위 설정
    lower_yellow = np.array([15, 30, 30])
    upper_yellow = np.array([35, 255, 255])
    # 범위 내의 부분(노란색)을 mask로 생성
    yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    # 커널 생성 후 침식, 팽창을 통해 노이즈 제거
    kernel = np.ones((5, 5), np.uint8)
    yellow_mask = cv2.erode(yellow_mask, kernel, iterations=1)
    yellow_mask = cv2.dilate(yellow_mask, kernel, iterations=1)

    # 노란색에 해당하는 contour 분리해 냄
    contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 스티커와 같은 모양의 contour만 분류

    # 흰 배경에 스티커 1개가 붙어 있는 사진 이미지를 불러 옴
    #reference_image = cv2.imread("/home/dan/Downloads/experiment/square_reference.jpg")
    reference_image = cv2.imread("/home/ktw/Downloads/experiment/square_reference.jpg")
    gray_reference_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)
    # 배경이 아닌 부분(스티커)만 분리해 냄
    _, reference_thresh = cv2.threshold(gray_reference_image, 127, 255, 0)

    # 가장 큰 contour를 찾거나, 정사각형 모양의 contour를 선택합
    reference_contours, _ = cv2.findContours(reference_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    reference_contour = reference_contours[0]  

    for contour in contours :#There are 3 casestours:
        area = cv2.contourArea(contour)
        # 최소 면적 기준을 넘은 contour만 고려
        if area > min_area:
            
            # 두 contour의 모양 일치 정도를 계산
            if shapeCheck(reference_contour, contour, shape_threshold):
                count += 1

            # 일치하는 정도가 임계값보다 낮은 경우, 해당 contour를 스티커 모양으로 간주하고 개수를 세어 출력
            
    # 선택 사항: 찾은 contour를 이미지에 그림
                cv2.drawContours(image, [contour], 0, (0, 255, 0), 2)
    #cv2.imwrite("/home/ktw/testdetect/test.jpg", image)

    print("Number of star-shaped stickers detected:", count)

    if count > 6:
        return "no shoe\n"
    elif count < 2:
        return "ok\n"
    else:
        return "sort please\n"

