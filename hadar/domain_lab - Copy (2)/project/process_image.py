import cv2
import matplotlib.pyplot as plt
import numpy as np
from os import remove
from pathlib import Path
from process_assist import process

LAB_IMAGES_RAW = "lab_images_raw/"
PROCESSED = "lab_images_processed/"
FROM_RAW = 'from_raw/'
PATH = "./"


# TODO: add dirtree structure for differentiationg between runs noting their order

def get_B_H_point(H=0, exposer_time=-4, counter=None):  # TODO: fix resolution and grab area
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_EXPOSURE, exposer_time)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)

    # ret, frame = cam.read()
    # if not ret:
    #     print('failed to grab image')
    #     return
    frame = cv2.imread('./not_stu_test.png')  # for testing

    name = process(PATH, frame, H, PROCESSED)
    cv2.imwrite(PATH + LAB_IMAGES_RAW + name, frame)  # TODO: add return of (B,H) point


if __name__ == '__main__':
    get_B_H_point(exposer_time=-2)
