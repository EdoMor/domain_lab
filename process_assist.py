from PIL import Image, ImageEnhance
import numpy as np
import datetime
import cv2


def gray_and_blurr(img, blurr: bool = True):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if blurr:
        gray_img = cv2.GaussianBlur(gray_img, (11, 11), 0)
    Img = Image.fromarray(gray_img)
    return Img


def thresh_binary(img, thresh: int = None):
    b = np.average(np.array(img))
    c = b + (80 - b) / 10
    threshold = c if thresh is None else thresh
    _, img_thres = cv2.threshold(np.asarray(img), threshold, 255, cv2.THRESH_BINARY)
    kernel = np.ones((2, 2), np.uint8)
    img_op = cv2.morphologyEx(img_thres, cv2.MORPH_OPEN, kernel, iterations=1)
    return Image.fromarray(img_op)


def new_enhance(img, chopsize: int = 50):
    img = gray_and_blurr(img)
    width, height = img.size
    for x0 in range(0, width, chopsize):
        for y0 in range(0, height, chopsize):
            x1 = x0 + chopsize if x0 + chopsize < width else width - 1
            y1 = y0 + chopsize if y0 + chopsize < height else height - 1
            box = (x0, y0, x1, y1)
            slc = img.crop(box)
            slc = thresh_binary(slc)
            img.paste(slc, (x0, y0))
    return img


def file_name_T_H_M(img: Image, H: float, counter=None) -> tuple:
    # str(now.month) + '_' + str(now.day) + '_' +
    now = datetime.datetime.now()
    time = str(now.day) + '_' + str(now.time()).replace('.', '_').replace(':', '_')
    time = time if counter is None else counter
    M = np.average(np.array(img))

    return f'C{time}_H{H}_M{M}.png'


def process(path, folder_name: str, img, H: float, counter=None) -> str:
    img = new_enhance(img)
    name = file_name_T_H_M(img, H, counter)
    img.save(path + folder_name + name)
    return name
