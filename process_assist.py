from PIL import Image
import numpy as np
import datetime
import cv2
import os
import constants
from process_image import mkdir

RAW = constants.RAW
PROCESSED = constants.PROCESSED
join = os.path.join


def detect_color(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # mask = cv2.inRange(hsv, (115, 115, 20), (165, 255, 255))
    mask = cv2.inRange(hsv, (115, 105, 20), (175, 255, 255))
    image = cv2.bitwise_not(mask)
    return image


def clear_dots(img):
    kernel = np.ones((2, 2), np.uint8)
    s = 1
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


def process(run_path: str):
    for filename in os.listdir(join(run_path, RAW)):
        img = cv2.imread(join(run_path, RAW, filename))
        img = detect_color(img)
        img = clear_dots(img)
        cv2.imwrite(join(run_path, PROCESSED, filename), img)


def is_empty_folder(path: str) -> bool:
    if os.path.exists(path) and os.path.isdir(path):
        if not os.listdir(path):
            return True
        else:
            return False
    else:
        return False


def scan_and_process(runs_path: str = './runs'):  # TODO: Deal with folders that are half full
    processed_set = set()
    while True:
        unprocessed_set = set(os.listdir(runs_path))-processed_set
        for filename in unprocessed_set:
            if is_empty_folder(join(runs_path, filename, PROCESSED)):
                process(join(runs_path, filename, PROCESSED))
                processed_set.add(filename)
# TODO: get processed_set (after forced ending)

## loud_data() returns 2 np arrays:
## 1) data : data[i] is a list of al the images in run_i, as np arrays
## 2) T_H_B_of_data : data[i][j] is the list: [T,H,B] of the j-th img in run_i


def loud_data(runs_path : str = './runs'):
    runs = os.listdir(runs_path)
    data = np.empty([1, len(runs)])
    T_H_B_of_data = np.empty([1, len(runs)])
    for i, run_folder in enumerate(runs):
        run_images_path = join(runs_path, run_folder, PROCESSED)
        run_images = os.listdir(run_images_path)
        run_data = np.empty([1, len(run_images)])
        T_H_B_of_run_data = np.empty([1, len(run_images)])
        for j, img in enumerate(run_images):
            run_data[j] = np.asarray(Image.open(join(run_images_path, img)))
            T_H_B_of_run_data[j] = img.split('_')
        data[i] = run_data
        T_H_B_of_run_data[i] = T_H_B_of_run_data
    return data, T_H_B_of_data







if __name__ == '__main__':
    scan_and_process()
