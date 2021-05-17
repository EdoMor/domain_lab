from PIL import Image, ImageEnhance
import numpy as np
import datetime


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


def file_name_T_H_M(img: Image, H: float, counter=None) -> tuple:
    now = datetime.datetime.now()
    # str(now.month) + '_' + str(now.day) + '_' +
    time = str(now.day) + '_' + str(now.time()).replace('.', '_').replace(':', '_')
    time = time if counter is None else counter
    M = np.average(np.array(img))

    return f'{time}_{H}_{M}.png', f'{time}_{H}_.png'


def process(path, temp, H: float, folder_name: str, counter=None) -> str:
    img = Image.open(path + temp)
    img = enhance(img)
    name_p, name_r = file_name_T_H_M(img, H, counter)
    img.save(path + folder_name + name_p)
    return name_r
