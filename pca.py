import numpy as np
from sklearn.decomposition import PCA
import cv2
import matplotlib.pyplot as plt


def smart_Gscale(img: np.array) -> np.array:
    # to vector
    V = img.reshape(-1, 3)

    # project to 1D
    pca = PCA(n_components=1).fit(V)
    V = pca.transform(V).reshape(-1)

    # normalize
    m = min(V)
    M = max(V) - m
    V = np.uint8((V - m) * 255 // M)

    # switch black & white
    V = 255 - V

    # return grey scale matrix
    return V.reshape(img.shape[:2])


if __name__ == '__main__':
    img = cv2.imread(r'C:\Users\97250\Desktop\LAB_B2\domain_lab\project\complete_run_test\pre\2.png')
    g = smart_Gscale(img)
    old = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(r'C:\Users\97250\Desktop\LAB_B2\domain_lab\project\folder_for_test\post\new.png', g)
    cv2.imwrite(r'C:\Users\97250\Desktop\LAB_B2\domain_lab\project\folder_for_test\post\old.png', old)
    print("done")

