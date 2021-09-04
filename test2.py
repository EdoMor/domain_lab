from PIL import Image
import numpy as np
import datetime
import cv2
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random


# my_run = r'F:\pycharm projects\domain lab\runs\run_8\raw'
# pics = os.listdir(my_run)
#
# volts=[]
#
# for i, pic_name in enumerate(pics):
#     volts.append(float(pic_name.split('_')[-1].replace('.png','')))


# x=range(len(volts))
# plt.plot(x,volts)
# plt.show()


# img = mpimg.imread(r'F:\pycharm projects\domain lab\runs\run_8\raw\1628506804.1056578_0.0.png')
# imgplot = plt.imshow(img)
# plt.show()

# left = 559
# top = 65
# right = 1380
# bottom = 906
#
# for pic_name in pics:
#     pic = Image.open(os.path.join(my_run, pic_name)).crop((left, top, right, bottom))
#     pic.save(os.path.join(r'F:\pycharm projects\domain lab\new_sample',pic_name))

# M=[]
# new_sample_drc = r'F:\pycharm projects\domain lab\new_sample'
# images = os.listdir(new_sample_drc)
# for img in images:
#     pic = Image.open(os.path.join(new_sample_drc, img))
#     picGray = pic.convert('L')
#     M.append(np.average(np.array(picGray)))
#
# plt.plot(volts,M)
# plt.show()

# img = mpimg.imread(r'F:\pycharm projects\domain lab\runs\run_121628590016.6035893_0.0.png')
# imgplot = plt.imshow(img)
# plt.show()

# def loud_data(runs_path: str = './runs'):
#     runs = os.listdir(runs_path)
#     data = np.empty([1, len(runs)])
#     T_H_B_of_data = np.empty([1, len(runs)])
#     for i, run_folder in enumerate(runs):
#         run_images_path = join(runs_path, run_folder, JPROCESSED)
#         run_images = os.listdir(run_images_path)
#         run_data = np.empty([1, len(run_images)])
#         T_H_B_of_run_data = np.empty([1, len(run_images)])
#         for j, img in enumerate(run_images):
#             run_data[j] = np.asarray(Image.open(join(run_images_path, img)))
#             T_H_B_of_run_data[j] = img.split('_')
#         data[i] = run_data
#         T_H_B_of_run_data[i] = T_H_B_of_run_data
#     return data, T_H_B_of_data


def data(runs_path: str = './runs'):
    runs = os.listdir(runs_path)
    input_img = np.empty([1, len(runs)*999])
    output_img = np.empty([1, len(runs)*999])
    jump = np.empty([1, len(runs)*999])
    for run in runs:
        run_images = os.listdir(os.path.join(runs_path,run))
        for img in run_images:



# jumps = np.array(random.sample(range(1, 50000), 1000)) / 55000
# s =5*np.sin(jumps)
# w=np.delete(s,0)
# w=np.append(w,0)
# n=s-w
# n = np.delete(n,-1)
# print(max(n))
# print(min(abs(n)))


# img = cv2.imread(r'F:\pycharm projects\domain lab\runs\run_14\1628590841.3998182_0.0.png')
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imwrite(r'./test_gray_size.png', gray)









