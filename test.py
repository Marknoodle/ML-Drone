from djitellopy import Tello
from time import sleep
import cv2
import matplotlib
import numpy as np
import math
from camera import ImgProcessing

from functions import *


#
#
# def test_mask(camera_index, color, gamma):
#     """
#         Function to test what hsv values are needed in a room.
#         Takes the argument camera_index and string color you are looking for.
#     """
#
#     # connect to the camera
#     cam = cv2.VideoCapture(camera_index)
#
#     # make a list of bars needed
#     bars = ['l_h_' + color, 'l_s_' + color, 'l_v_' + color,
#             'u_h_' + color, 'u_s_' + color, 'u_v_' + color]
#
#     # create the track bars
#     win_name = color + '_track'
#     cv2.namedWindow(win_name)
#     cv2.createTrackbar(bars[0], win_name, 0, 179, nothing)
#     cv2.createTrackbar(bars[1], win_name, 0, 255, nothing)
#     cv2.createTrackbar(bars[2], win_name, 0, 255, nothing)
#     cv2.createTrackbar(bars[3], win_name, 179, 179, nothing)
#     cv2.createTrackbar(bars[4], win_name, 255, 255, nothing)
#     cv2.createTrackbar(bars[5], win_name, 255, 255, nothing)
#
#     # continue updating frames
#     while True:
#         ret, frame = cam.read()
#         if ret:
#             frame = gamma_trans(frame, gamma)
#
#             hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#
#             lower_mask = np.array([cv2.getTrackbarPos(bars[0], win_name),
#                                    cv2.getTrackbarPos(bars[1], win_name),
#                                    cv2.getTrackbarPos(bars[2], win_name)])
#             upper_mask = np.array([cv2.getTrackbarPos(bars[3], win_name),
#                                    cv2.getTrackbarPos(bars[4], win_name),
#                                    cv2.getTrackbarPos(bars[5], win_name)])
#
#             mask = cv2.inRange(hsv, lower_mask, upper_mask)
#             result = cv2.bitwise_and(frame, frame, mask=mask)
#
#             mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
#             combined = np.concatenate((mask, result), axis=1)
#             cv2.imshow(win_name, combined)
#
#             if cv2.waitKey(2) == ord('q'):
#                 cam.release()
#                 cv2.destroyAllWindows()
#                 break



