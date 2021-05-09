import cv2
from os import remove
from pathlib import Path
from process_assist import process

TEMP = "temp.png"
LAB_IMAGES = "lab_images/"
PATH = str(Path().absolute()) + '\\'


def get_H_M_point(H=0, exposer_time=-6):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_EXPOSURE, exposer_time)
    ret, frame = cam.read()
    if not ret:
        print('failed to grab image')
        return
    # frame = cv2.imread('test.png', 2)  # test
    cv2.imwrite(PATH + TEMP, frame)
    name = process(PATH, TEMP, H)
    remove(PATH + TEMP)  # remove temp
    cv2.imwrite(PATH + LAB_IMAGES + name, frame)


if __name__ == '__main__':
    get_H_M_point()
