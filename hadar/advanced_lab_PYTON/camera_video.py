# run to get video:
# press 'q' to stop:

import cv2, time
video = cv2.VideoCapture(1, cv2.CAP_DSHOW)
video.set(15, 0.1)

while True:
    check, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('cap', gray)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()