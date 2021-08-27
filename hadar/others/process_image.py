import cv2
import matplotlib.pyplot as plt
import numpy as np
from os import remove
from pathlib import Path
import datetime
import time
import os
from process_assist import process
import constants

ROOT = constants.ROOT
RAW = constants.RAW
PROCESSED = constants.PROCESSED
FROM_RAW = constants.FROM_RAW
PATH = constants.PATH
FAILED = constants.FAILED
RUNFILE = constants.RUNFILE


# TODO: add dirtree structure for differentiationg between runs noting their order
# TODO: fix resolution and grab area

def write(filepath, filename, filecontence, index=0):
    if os.path.exists(os.path.join(filepath, filename)):
        filename = '.'.join(filename.split('.')[:-1]) + str(index) + '.' + filename.split('.')[-1]
        write(filepath, filename, filecontence, index + 1)
    else:
        try:
            cv2.imwrite(os.join(filepath, filename), filecontence)
            return True
        except:
            print('failed to save file' + filename)
            return False


def get_run(path, file):
    filepath = os.path.join(path, file)
    if not os.path.exists(filepath):
        uin = input('run counter file ' + str(filepath) + ' not found\nare you shure you want to create it?(y/n): ').lower()
        if uin == 'yes' or uin == 'y':
            with open(filepath, 'w') as fo:
                fo.write(str(0))
        else:
            raise RuntimeError('file ' + str(filepath) + ' not found')
    with open(filepath, 'r') as fo:
        run = fo.read()
    return int(run)


def incument_run(path, file):
    filepath = os.path.join(path, file)
    run = get_run(path, file)
    with open(filepath, 'w') as fo:
        fo.write(str(run + 1))
    return True

def mkdir(path):
    dirs=path.split('/')
    cdir=''
    for dir in dirs:
        cdir=os.path.join(cdir,dir)
        if not os.path.exists(cdir):
            os.mkdir(cdir)


def get_H_B_point(H: float = 0, exposer_time: int = -4, counter: int = None, run: int = -1) -> bool:
    run = get_run(ROOT, RUNFILE)
    dirName = PATH + str(run)

    for name in ['', PROCESSED, RAW]:
        try:
            mkdir(dirName + name)
        except:
            print('did not make dir')
            print(dirName + name)
            return False

    try:
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    except:
        print('video capture failed')
        return False

    try:
        cam.set(cv2.CAP_PROP_EXPOSURE, exposer_time)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944)
    except:
        print('problem with setting the camera')

    ret, frame = cam.read()
    if not ret:
        print('failed to grab image')
        return False

    # frame = cv2.imread('./stu_test.png')  # for testing

    # try:
    #     name = process(dirName, PROCESSED, frame, H, counter)
    # except:
    #     print('problem with process')
    # now = datetime.datetime.now()
    # time = str(now.day) + '_' + str(now.time()).replace('.', '_').replace(':', '_')
    now = time.time()
    counter = now if counter is None else counter
    name = f'{counter}_{H}.png'

    try:
        cv2.imwrite(dirName + RAW + name, frame)  # TODO: add return of (B,H) point
    except:
        print('could not save RAW img')
        return False

    return True


if __name__ == '__main__':
    get_H_B_point(exposer_time=-2, counter=2)
