import cv2
from process_assist import process
import matplotlib.pyplot as plt
import numpy as np

TEMP = "temp.png"
LAB_IMAGES = "lab_images/"
PATH = "./"


# TODO: add dirtree structure for differentiationg between runs noting their order

def get_B_H_point(B=0, exposer_time=-4, debug=False):  # TODO: fix resolution and grab area
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_EXPOSURE, exposer_time)
    # todo:
    if debug:
        while True:
            ret, frame = cam.read()
            if not ret:
                print('failed to grab image')
                exit(1)
            plt.ion()
            plt.imshow(np.array(frame))
            plt.pause(0.05)
    else:
        ret, frame = cam.read()
        if not ret:
            print('failed to grab image')
            return
        # frame = cv2.imread('test.png', 2)  # todo temp

    cv2.imwrite(PATH + TEMP, frame)
    name = process(PATH, TEMP, B)
    cv2.imwrite(PATH + LAB_IMAGES + name, frame)  # TODO: add return of (B,H) point


if __name__ == '__main__':
    get_B_H_point(exposer_time=-4, debug=True)
