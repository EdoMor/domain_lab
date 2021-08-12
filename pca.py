from sklearn.decomposition import PCA
from PIL import Image
from numpy import asarray
import numpy as np
import cv2
import matplotlib.pyplot as plt


def smart_Gscale(img):
    # open image
    data = asarray(img)[:, :, [0, 1, 2]]

    # save shape
    shape = data.shape[:2]

    # smart grey scale
    # to vector
    X = data.reshape(-1, 3)
    # project to 1D
    pca = PCA(n_components=1).fit(X)
    X = pca.transform(X).reshape(-1)
    # normalize
    m = min(X)
    M = max(X)-m
    X = np.uint8((X-m)*255//M)
    # to matrix
    data = X.reshape(shape)

