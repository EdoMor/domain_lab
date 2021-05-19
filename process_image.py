import cv2
import matplotlib.pyplot as plt
import numpy as np
from os import remove
from pathlib import Path
from process_assist import process

TEMP = "temp.png"
LAB_IMAGES_RAW = "lab_images_raw/"
PROCESSED = "lab_images_processed/"
FROM_RAW = 'from_raw/'
PATH = "./"


# TODO: add dirtree structure for differentiationg between runs noting their order

def get_B_H_point(H=0, exposer_time=-4, counter=None):  # TODO: fix resolution and grab area
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_EXPOSURE, exposer_time)
    # todo:
    # if False:  # debug:
    #     while True:
    #         ret, frame = cam.read()
    #         if not ret:
    #             print('failed to grab image')
    #             exit(1)
    #         plt.ion()
    #         plt.imshow(np.array(frame))
    #         plt.pause(0.05)
    # else:
    ret, frame = cam.read()
    if not ret:
        print('failed to grab image')
        return
    # frame = cv2.imread(test.png', 2)  # for testing

    cv2.imwrite(PATH + TEMP, frame)
    name = process(PATH, TEMP, H, PROCESSED)
    cv2.imwrite(PATH + LAB_IMAGES_RAW + name, frame)  # TODO: add return of (B,H) point
    # new code
    frame = cv2.imread(PATH + LAB_IMAGES_RAW + name, 2)
    cv2.imwrite(PATH + TEMP, frame)
    process(PATH, TEMP, H, FROM_RAW, counter)


if __name__ == '__main__':
    get_B_H_point(exposer_time=-2)
