import cv2
import numpy as np
import datetime
from PIL import Image
import os
import matplotlib.pyplot as plt

now = datetime.datetime.now()
time = str(now.day) + '_' + str(now.time()).replace('.', '_').replace(':', '_')

def gray_and_blurr(img, blurr:bool=True):
    gray_img = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2GRAY)
    if blurr:
        gray_img = cv2.GaussianBlur(gray_img, (21, 21), 0)
    gray_img = Image.fromarray(gray_img)
    return gray_img


def thresh_binary(img, thresh: int = None):
    b = np.average(np.array(img))
    c = b + (30 - b) / 10
    threshhold = c if thresh is None else thresh
    _, img_thres = cv2.threshold(np.asarray(img), threshhold, 255, cv2.THRESH_BINARY)
    # kernel = np.ones((2, 2), np.uint8)
    # img_op1 = cv2.morphologyEx(img_thres, cv2.MORPH_OPEN, kernel, iterations=1)
    # # img_op2 = cv2.morphologyEx(img_thres, cv2.MORPH_CLOSE, kernel, iterations=1)
    return Image.fromarray(img_thres)

def new_enhance(img, chopsize:int=100):
    width, height = img.size
    for x0 in range(0, width, chopsize):
        for y0 in range(0, height, chopsize):
            x1 = x0 + chopsize if x0 + chopsize < width else width - 1
            y1 = y0 + chopsize if y0 + chopsize < height else height - 1
            box = (x0, y0, x1, y1)
            slc = img.crop(box)
            slc = thresh_binary(slc)
            img.paste(slc, (x0, y0))
    # img.save('./runs/test/'+f'{time}.png')
    return img


def clean(img):
    kernel = np.ones((5, 5), np.uint8)
    img_op1 = cv2.morphologyEx(np.asarray(img), cv2.MORPH_OPEN, kernel, iterations=1)
    img_op2 = cv2.morphologyEx(img_op1, cv2.MORPH_CLOSE, kernel, iterations=1)
    return Image.fromarray(img_op2)


def shmuel_process(img, dark_stu_img, light_stu_img, blur:bool=False, epsilon=0.05):
    img, dark_stu_img, light_stu_img = gray_and_blurr(img, blur), gray_and_blurr(dark_stu_img, blur), gray_and_blurr(light_stu_img, blur)
    if np.shape(img) != np.shape(dark_stu_img):
        return print("error: dark-saturated image is not the same size as image")
    if np.shape(img) != np.shape(light_stu_img):
        return print("error: light-saturated image is not the same size as image")
    img_op = (img - dark_stu_img) / light_stu_img  # TODO return -light_stu_img

    height, width = np.shape(img)
    None_img = img_op.copy()
    av = np.average(img_op)
    for j in range(width):
        for i in range(height):
            if np.abs(img_op[i][j] - av) <= epsilon:
                None_img[i][j] = 0

    _, img_thresh = cv2.threshold(img_op, av, 255, cv2.THRESH_BINARY)
    _, None_img_thresh = cv2.threshold(None_img, np.average(None_img), 255, cv2.THRESH_BINARY)

    return np.average(None_img_thresh), img_thresh, None_img_thresh



if __name__ == '__main__':
    # new_d_test = cv2.imread('./new_b_test.jpeg')
    # g = gray_and_blurr(new_d_test)
    # binery = new_enhance(g)
    # binery = thresh_binary(g)
    # binery.show()
    # img = cv2.imread('./smuel_process_test/un_stu.jpg')
    # dark_stu_img = cv2.imread('./smuel_process_test/dark.jpg')
    # light_stu_img = cv2.imread('./smuel_process_test/light.jpg')
    # M, pr, None_pr = shmuel_process(img, dark_stu_img, light_stu_img, False, epsilon=0.25)
    # pr = Image.fromarray(pr)
    # None_pr = Image.fromarray(None_pr)
    # pr.show()
    # None_pr.show()

    # left = 510
    # top = 580
    # right = 1820
    # bottom = 1750
    # light = Image.open('./smuel_process_test/complete_run/1623758745.1653996_-4.9.png')
    # dark = Image.open('./smuel_process_test/complete_run/1623758543.9846883_4.9.png')
    # path = '.\smuel_process_test\complete_run'
    # path_for_saving = '.\smuel_process_test\processed'
    # M = []
    # V = []
    # for i, img_name in enumerate(os.listdir(path)):
    #     img = Image.open(os.path.join(path, img_name))
    #     img = img.crop((left, top, right, bottom))
    #     img = gray_and_blurr(img)
    #     img = new_enhance(img)
    #     m = np.average(np.asarray(img))
    #     M.append(m)
    #     V.append(float(img_name.split('_')[-1].replace('.png', '')))
    #     a = os.path.join(path_for_saving, img_name.replace('.png', '') + str(m) + '.png')
    #     cv2.imwrite(a, np.asarray(img))
    # print(M)
    # print(V)
    # plt.plot(2.4 * np.array(V), M, '-o')
    # plt.show()

    img = Image.open('./smuel_process_test/complete_run/1623758448.0745485_0.61413.png')
    img.convert("L")
    img.show()












