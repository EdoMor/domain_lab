from PIL import Image, ImageEnhance
import numpy as np
import datetime

PREPROCESSED = "lab_images_preprocessed/"


def enhance(img: Image) -> Image:
    chopsize = 50
    width, height = img.size
    for x0 in range(0, width, chopsize):
        for y0 in range(0, height, chopsize):
            x1 = x0 + chopsize if x0 + chopsize < width else width - 1
            y1 = y0 + chopsize if y0 + chopsize < height else height - 1
            box = (x0, y0, x1, y1)
            slc = img.crop(box)
            slc = ImageEnhance.Contrast(slc).enhance(1000)
            img.paste(slc, (x0, y0))
    img = ImageEnhance.Contrast(img).enhance(100)
    fn = lambda x: 255 if x > 100 else 0
    img = img.convert('L').point(fn, mode='1')
    return img


def find_H(img: Image) -> float:
    H = np.average(np.array(img))
    return H


def file_name_T_B_H(img: Image, B: float) -> str:
    now = datetime.datetime.now()
    time = str(now.month) + '_' + str(now.day) + '_' + str(now.time()).replace('.', '_').replace(':', '_')
    H = find_H(img)
    return f'{time}_{B}_{H}.png'


def process(path, temp, B: float) -> str:
    img = Image.open(path + temp)
    img = enhance(img)
    name = file_name_T_B_H(img, B)
    img.save(path + PREPROCESSED + name)
    return name

# class Process:
#
#     def __init__(self, path, temp, B: float):
#         self.B = B
#         self.img = Image.open(path + temp)
#         self.__enhance()
#         self.name = self.__file_name_T_B_H()
#         self.img.save(path + PREPROCESSED + self.name)
#
#     def __enhance(self):
#         chopsize = 50
#         width, height = self.img.size
#         for x0 in range(0, width, chopsize):
#             for y0 in range(0, height, chopsize):
#                 x1 = x0 + chopsize if x0 + chopsize < width else width - 1
#                 y1 = y0 + chopsize if y0 + chopsize < height else height - 1
#                 box = (x0, y0, x1, y1)
#                 slc = self.img.crop(box)
#                 slc = ImageEnhance.Contrast(slc).enhance(1000)
#                 self.img.paste(slc, (x0, y0))
#         self.img = ImageEnhance.Contrast(self.img).enhance(100)
#         fn = lambda x: 255 if x > 100 else 0
#         self.img = self.img.convert('L').point(fn, mode='1')
#
#     def file_name_T_B_H(self) -> str:
#         def H():
#             H_ = 1
#             return H_
#
#         def time():
#             now = datetime.datetime.now()
#             return str(now.month) + '_' + str(now.day) + '_' + str(now.time()).replace('.', '_').replace(':', '_')
#
#         return f'{time()}_{self.B}_{H()}.png'
#
# def process(path, temp, B: float):
#     self = Process(path, temp, B)
#     return self.name
