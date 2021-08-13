import numpy as np
from sklearn.decomposition import PCA
import cv2
import cv2 as cv
import matplotlib.pyplot as plt
import os


def test(v):
    v = np.int8(v)
    m, M = min(v), max(v) + 1
    lst = np.zeros(M - m)

    for c in v:
        lst[c + m] += 1

    plt.plot(range(m, M), lst)
    plt.show()


def smart_Gscale(img: np.array) -> np.array:
    # to vector
    V = img.reshape(-1, 3)

    # project to 1D
    pca = PCA(n_components=1).fit(V)
    V = pca.transform(V).reshape(-1)

    # test
    # test(V)
    # v = cv2.threshold(0, V)

    # normalize
    # m = min(V)
    # M = max(V) - m
    # V = np.uint8((V - m) * 255 // M)
    #
    # # switch black & white
    # V = 255 - V

    # return grey scale matrix
    img = V.reshape(img.shape[:2])
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    return img

# this is the binarythaitian that works!!:
def gaussian_blur_otzu(img):
    # Otsu's thresholding after Gaussian filtering
    blur = cv.GaussianBlur(img, (5, 5), 0)
    ret3, binary = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    return binary

# count number of images in the run directory
def data_size(runs_path: str = './runs')->int:
    runs = os.listdir(runs_path)
    data_size = 0
    for run in runs:
        run_images = os.listdir(os.path.join(runs_path, run))
        data_size += len(run_images)-1
    return  data_size


# gets an img name and returns only the volt
def get_volt_from_img_name(name:str)->float:
    return float(name.split('_')[-1].replace('.png',''))

# gets the run dir and returns:
# (1) a list of all the input pics
# (2) a list of all the corasponding output pics,
# (3) a matrix with 2 rows: the first has the volt of the corasponding input pic,
#                           the second has the volt of the corasponding output pic
def data(runs_path: str = './runs'):
    runs = os.listdir(runs_path)
    input_pics = np.empty(data_size(runs_path))
    output_pics = np.empty(data_size(runs_path))
    vals = np.empty([2,data_size(runs_path)])
    loaded_input_pics_counter = 0
    loaded_output_pics_counter = 0
    for run_num, run in enumerate(runs):
        run_images = os.listdir(os.path.join(runs_path, run))
        for pic_num, pic in enumerate(run_images[:-1]):
            input_pics[loaded_input_pics_counter+pic] = cv2.imread(os.path.join(runs_path, run, pic))
            vals[1, loaded_input_pics_counter+pic] = get_volt_from_img_name(pic)
            loaded_input_pics_counter+=1
        for pic_num, pic in enumerate(run_images[1:]):
            output_pics[loaded_output_pics_counter+pic] = cv2.imread(os.path.join(runs_path, run, pic))
            vals[2, loaded_input_pics_counter+pic] = get_volt_from_img_name(pic)
            loaded_output_pics_counter+=1
    return input_pics, output_pics, vals


if __name__ == '__main__':
    path = r'C:\Users\97250\Desktop\LAB_B2\domain_lab\project\folder_for_test\pre\1628590845.252835_4.20919.png'
    img = cv2.imread(path, 0)
    blur = cv.GaussianBlur(img, (5, 5), 0)
    cv2.imshow('image', blur)
    cv2.waitKey(0)
# img = cv2.imread(r'C:\Users\97250\Desktop\LAB_B2\domain_lab\project\complete_run_test\pre\2.png', 0)
