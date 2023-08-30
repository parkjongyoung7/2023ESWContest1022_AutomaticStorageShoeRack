import cv2
import numpy as np
import time

color_ranges = {
        'white': ([0, 0, 200], [180, 60, 255]),
        'black': ([0, 0, 0], [180, 255, 50]),
        'red1': ([0, 70, 50], [15, 255, 255]),
        'red2': ([165, 70, 50], [180, 255, 255]),
        'blue': ([0, 180, 55], [20, 255, 200]),
        'green': ([40, 60, 55], [90, 255, 255]),
    }
priority_colors = ['red', 'blue', 'green']
other_colors = ['white', 'black']

def main_color(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, dsize = (500, 500), interpolation=cv2.INTER_AREA)
    blurred = cv2.GaussianBlur(image, (15, 15), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    color_areas = {}
    for color, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        area = sum(cv2.contourArea(cnt) for cnt in contours)
        
        # red의 경우 hue가 0과 180 양쪽 끝에 위치에 있어 두 경우를 합하여 구함
        if color == 'red1':
            red1_area = area
            continue
        if color == 'red2':
            color_areas['red'] = red1_area = area
            continue
            
        color_areas[color] = area

    print(color_areas)
    main_color = determine_main_color(color_areas)
    return main_color

def determine_main_color(color_areas):
    #print(color_areas['green'])
    
    # white의 경우 감지가 많이 되면 우선 리턴하는 것이 결과가 더 좋음
    if color_areas['white'] > 10000:
        return 'white'
    
    # 우선순위가 있는 색상들을 먼저 확인합니다.
    
    max_priority_area = 7000
    main_color = None
    for color in priority_colors:
        if color_areas[color] > max_priority_area:
            max_priority_area = color_areas[color]
            main_color = color
    #print(main_color)

    # 우선순위가 있는 색상이 없는 경우, 다른 색상들을 확인합니다.
    if main_color == None:
        '''
        max_area = 0
        for color in other_colors:
            if color_areas[color] > max_area:
                max_area = color_areas[color]
                main_color = color
        '''
        if color_areas['white'] > 10000:
            return 'white'
        else:
            return 'black'
    return main_color

#image_path = "./color/green/10.png"
#result = main_color(image_path)
        
#print(f"The main color of the shoe is: {result}")