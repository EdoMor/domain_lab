import cv2, time

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
video.set(cv2.CAP_PROP_EXPOSURE,-3)

# video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

video.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)

# video.open(0, CAP_DSHOW)

check, frame = video.read()

#gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

print(check)

print(video.get(cv2.CAP_PROP_FRAME_WIDTH))
print(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

cv2.imshow('img1', frame)
cv2.waitKey(0)

video.release()


