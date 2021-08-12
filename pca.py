import numpy as np
from sklearn.decomposition import PCA


def smart_Gscale(img: np.array) -> np.array:
    # save shape
    shape = img.shape[:2]

    # to vector
    v = img.reshape(-1, 3)

    # project to 1D
    pca = PCA(n_components=1).fit(v)
    v = pca.transform(v).reshape(-1)
    # normalize
    m = min(v)
    M = max(v) - m
    v = np.uint8((v - m) * 255 // M)

    # to matrix
    return v.reshape(shape)
