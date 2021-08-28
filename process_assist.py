from PIL import Image
import numpy as np
import datetime
import cv2
import os
import constants
import pca

JRAW = constants.JRAW
JPROCESSED = constants.JPROCESSED
join = os.path.join


def detect_color(img):  # TODO: normalize image and widen color range
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # mask = cv2.inRange(hsv, (115, 115, 20), (165, 255, 255))
    mask = cv2.inRange(hsv, (115, 105, 20), (175, 255, 255))
    # mask = cv2.inRange(hsv, (125, 255*0.6, 255*0.2), (175, 255*0.8, 255*0.8))
    image = cv2.bitwise_not(mask)
    return image


def clear_dots(img):
    kernel = np.ones((2, 2), np.uint8)
    s = 1
    if np.average(np.array(img)) > 127.5:
        img_op1 = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=s)
        img_op2 = cv2.morphologyEx(img_op1, cv2.MORPH_CLOSE, kernel, iterations=s)
    else:
        img_op1 = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=s)
        img_op2 = cv2.morphologyEx(img_op1, cv2.MORPH_CLOSE, kernel, iterations=s)
    return img_op2


def file_name_T_H_M(img: Image, H: float, counter=None) -> str:
    # str(now.month) + '_' + str(now.day) + '_' +
    now = datetime.datetime.now()
    time = str(now.day) + '_' + str(now.time()).replace('.', '_').replace(':', '_')
    time = time if counter is None else counter
    M = np.average(np.array(img))
    return f'C{time}_H{H}_M{M}.png'


def image_process(source_path: str):
    dir = os.path.dirname(source_path)
    filename = os.path.split(source_path)[-1]
    if not os.path.exists(os.path.join(dir, 'raw')):
        os.mkdir(os.path.join(dir, 'raw'))

    if not os.path.exists(os.path.join(dir, 'raw')):
        os.mkdir(os.path.join(dir, 'processed'))

    if 'raw' in source_path:
        destination_path = source_path.replace('raw',
                                                'processed')  # TODO: protect agaist 'raw' apearing more then once
    else:
        os.rename(source_path, os.path.join(dir, 'raw', filename))
        source_path =os.path.join(dir, 'raw', filename)
        destination_path = source_path.replace('raw', 'processed')

    img = cv2.imread(source_path)
    if len(img.shape) != 2:  # TODO: see if the smart Gscale can be used (it currently cannot)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = pca.gaussian_blur_otzu(img)
    M = np.average(np.array(img))
    cv2.imwrite(destination_path.replace('.png', '_' + str(M) + '.png').replace('/', '\\'), img)


def process(run_path: str):
    for filename in os.listdir(join(run_path, JRAW)):
        image_process(join(run_path, JRAW, filename))


def is_empty_folder(path: str) -> bool:
    if os.path.exists(path) and os.path.isdir(path):
        if not os.listdir(path):
            return True
        else:
            return False
    else:
        return False


def scan_and_process(runs_path: str = './runs'):  # TODO: Deal with folders that are half full
    processed_set = set()
    while True:
        unprocessed_set = set(os.listdir(runs_path)) - processed_set
        for filename in unprocessed_set:
            if is_empty_folder(join(runs_path, filename, JPROCESSED)):
                process(join(runs_path, filename, JPROCESSED))
                processed_set.add(filename)


# TODO: get processed_set (after forced ending)

## loud_data() returns 2 np arrays:
## 1) data : data[i] is a list of al the images in run_i, as np arrays
## 2) T_H_B_of_data : data[i][j] is the list: [T,H,B] of the j-th img in run_i


def loud_data(runs_path: str = './runs'):
    runs = os.listdir(runs_path)
    data = np.empty([1, len(runs)])
    T_H_B_of_data = np.empty([1, len(runs)])
    for i, run_folder in enumerate(runs):
        run_images_path = join(runs_path, run_folder, JPROCESSED)
        run_images = os.listdir(run_images_path)
        run_data = np.empty([1, len(run_images)])
        T_H_B_of_run_data = np.empty([1, len(run_images)])
        for j, img in enumerate(run_images):
            run_data[j] = np.asarray(Image.open(join(run_images_path, img)))
            T_H_B_of_run_data[j] = img.split('_')
        data[i] = run_data
        T_H_B_of_run_data[i] = T_H_B_of_run_data
    return data, T_H_B_of_data


def gray_and_blurr(img, blurr: bool = True):
    gray_img = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2GRAY)
    if blurr:
        gray_img = cv2.GaussianBlur(gray_img, (21, 21), 0)
    return gray_img


def shmuel_process(img, dark_stu_img, blur: bool = False, epsilon=0.25):
    img, dark_stu_img = gray_and_blurr(img, blur), gray_and_blurr(dark_stu_img, blur)
    if np.shape(img) != np.shape(dark_stu_img):
        return print("error: dark-saturated image is not the same size as image")
    img_op = img / dark_stu_img
    av = np.average(img_op)

    height, width = np.shape(img)
    for j in range(width):
        for i in range(height):
            if np.abs(img_op[i][j] - av) < epsilon:
                img_op[i][j] = 0

    _, img_thresh = cv2.threshold(img_op, np.average(img_op), 255, cv2.THRESH_BINARY)

    return np.average(img_thresh), img_thresh


if __name__ == '__main__':
    # light_stu_img = cv2.imread('./runs_tor/run_55/raw/1623242427.5696151_3.90357.png')
    # dark_stu_img = cv2.imread('./runs_tor/run_55/raw/1623242448.2937782_-3.91397.png')
    # img = cv2.imread('./runs_tor/run_55/raw/1623242440.114422_-0.03447.png')
    # M, processed_image = shmuel_process(img, dark_stu_img)
    # process_image = Image.fromarray(processed_image)
    # process_image.show()
    M = []
    v = []
    path = r'.\runs\run_3\raw'
    stu_path = r'.\runs\run_3\raw\1623758543.9846883_4.9.png'
    for i, img in enumerate(os.listdir(path)):
        a = shmuel_process(cv2.imread(os.path.join(path, img)), cv2.imread(stu_path))
        cv2.imwrite(os.path.join(path, img).replace('raw', 'processed'), a[1])
        M.append(a[0])
        v.append(float(img.rsplit('.', 1)[0].rsplit('_', 1)[-1]))
    import matplotlib.pyplot as plt

    np.save(r'.\runs\run_3\vM.txt', np.array([v, M]))
    plt.plot(2.4 * np.array(v), M, '.')
    plt.show()
