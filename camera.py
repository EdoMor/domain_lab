import cv2
import matplotlib.pyplot as plt


cap=cv2.VideoCapture(0,700)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,2592)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1994)

while 1:
    _,frame=cap.read()
    plt.imshow(frame)
    plt.pause(1/24)