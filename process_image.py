import cv2
import matplotlib.pyplot as plt
import numpy as np
from os import remove
from pathlib import Path
import datetime
import os
from process_assist import process

RAW = "/raw/"
PROCESSED = "/processed/"
FROM_RAW = 'from_raw'
PATH = './runs/run_'
FAILED = 'FAILED'


# TODO: add dirtree structure for differentiationg between runs noting their order
# TODO: fix resolution and grab area

def get_H_B_point(H: float = 0, exposer_time: int = -4, counter: int = None, run: int = -1) -> bool:
    dirName = PATH + str(run)

    for name in ['', PROCESSED, RAW]:
        if not os.path.exists(dirName + name):
            try:
                os.mkdir(dirName + name)
            except:
                print('did not make dir')
                return False

    try:
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    except:
        print('video capture failed')
        return False

    try:
        cam.set(cv2.CAP_PROP_EXPOSURE, exposer_time)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)
    except:
        print('problem with setting the camera')

    # ret, frame = cam.read()
    # if not ret:
    #     print('failed to grab image')
    #     return False

    frame = cv2.imread('./stu_test.png')  # for testing

    try:
        name = process(dirName, PROCESSED, frame, H, counter)
    except:
        print('problem with process')
        now = datetime.datetime.now()
        time = str(now.day) + '_' + str(now.time()).replace('.', '_').replace(':', '_')
        counter = time if counter is None else counter
        name = f'C{counter}_H{H}_{FAILED}.png'

    try:
        cv2.imwrite(dirName + RAW + name, frame)  # TODO: add return of (B,H) point
    except:
        print('could not save RAW img')
        return False

    return True


if __name__ == '__main__':
    get_H_B_point(exposer_time=-2, counter=2)
