# Vision Based Navigation Research
# Augusta University School of Computer and Cyber Sciences
# Date Started 5/14/21
###############################################################################

from djitellopy import Tello
import cv2
import matplotlib
import numpy as np
import math
from functions import *

###############################################################################
# Main
###############################################################################

# define the empty list for centers
red_center, blue_center, green_center = [], [], []

# continue taking pictures until a red, green, and blue center have been located
while not red_center and not blue_center and not green_center:
    print("Calculating Centers\n")
    red_center, blue_center, green_center, rectangles = find_all_centers(1)

print(f" Centers Found \nRed Center: {red_center}\nBlue Center: {blue_center}\nGreen Center: {green_center}\n")

# show the picture of the rectangles
cv2.imshow('rectangles', rectangles)
cv2.waitKey(0)

mid_point = find_mid_point(green_center, red_center)
print(f"Mid point: {mid_point}\n")

red_rtm = move_origin(red_center, mid_point)
print(f"red relative to midpoint: {red_rtm}\n")

green_rtm = move_origin(green_center, mid_point)
print(f"green relative to midpoint: {green_rtm}\n")


blue_rtm = move_origin(blue_center, mid_point)
print(f"blue relative to midpoint: {blue_rtm}\n")

green_rotation = calculate_angle(green_rtm)
blue_rotation = calculate_angle(blue_rtm)
print(f"Blue rotation: {blue_rotation}\nGreen rotation: {green_rotation}\n")

rotation = blue_rotation - green_rotation
print(f"Rotation: {rotation}")



#tello = Tello()

#tello.set_speed(10)
#tello.takeoff()
#tello.move_forward(int(cmdistance))
#tello.land()






