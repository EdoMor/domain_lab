from PIL import Image, ImageEnhance
import numpy as np
import datetime
import cv2

def detect_color(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # mask = cv2.inRange(hsv, (115, 115, 20), (165, 255, 255))
    mask = cv2.inRange(hsv, (115, 105, 20), (175, 255, 255))
    image = cv2.bitwise_not(mask)
    return image


def clear_dots(img):
    kernel = np.ones((2, 2), np.uint8)
    s=1
    if np.average(np.array(img)) > 127.5:
        img_op1 = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=s)
        img_op2 = cv2.morphologyEx(img_op1, cv2.MORPH_CLOSE, kernel, iterations=s)
    else:
        img_op1 = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=s)
        img_op2 = cv2.morphologyEx(img_op1, cv2.MORPH_CLOSE, kernel, iterations=s)
    return img_op2


def file_name_T_H_M(img: Image, H: float, counter=None) -> str:
    # str(now.month) + '_' + str(now.day) + '_' +
    now = datetime.datetime.now()
    time = str(now.day) + '_' + str(now.time()).replace('.', '_').replace(':', '_')
    time = time if counter is None else counter
    M = np.average(np.array(img))
    return f'C{time}_H{H}_M{M}.png'


def process(path, folder_name: str, img, H: float, counter=None) -> str:
    img = detect_color(img)
    img = clear_dots(img)
    name = file_name_T_H_M(img, H, counter)
    cv2.imwrite(path + folder_name + name, img)
    return name