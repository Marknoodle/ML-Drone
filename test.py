import cv2
import numpy as np
from camera import ImgProcessing, RealsenseProcessing
import threading
from calculations import Calculations
from djitellopy import Tello


def thread_process(tello_o):
    while True:
        print(f'{tello_o.get_height()} - thread')


tello = Tello()
tello.connect()
tello.takeoff()

t1 = threading.Thread(target=thread_process, args=[tello])
t1.start()
while True:
    print(f'{tello.get_height()} - main')



# def live_stream(cam, update_delay):
#     out = cv2.VideoWriter('output_video.avi', cv2.VideoWriter_fourcc(*'XVID'), 24, (1920,1080))
#
#     while True:
#         ret, img = processing.cam.read()
#         cv2.imshow('live_stream', img)
#         out.write(img)
#         if cv2.waitKey(update_delay) & 0xFF == ord('q'):
#             break
#
# processing = ImgProcessing(0)
#
#
# live_stream(processing, 1)
# counter = 0
# for x in range (5):
#     win_name = f'img_{counter}'
#     img = processing.get_ref_image()
#     cv2.imshow(win_name, img)
#     counter += 1
# cv2.waitKey(0)
