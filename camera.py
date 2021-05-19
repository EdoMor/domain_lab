import cv2, time

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
video.set(cv2.CAP_PROP_EXPOSURE,-6)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

check, frame = video.read()
gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

cv2.imshow('img1', gray_frame)
cv2.waitKey(0)

video.release()


