from camera import RealsenseProcessing
import cv2
# cam = RealsenseProcessing()
cam = cv2.VideoCapture(1)
while True:

    ret, img = cam.read()
    # img = cam.get_ref_image()

    cv2.imshow('img', img)
    cv2.waitKey(2)