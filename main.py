# Vision Based Navigation Research
# Augusta University School of Computer and Cyber Sciences
# Date Started 5/14/21
###############################################################################

from djitellopy import Tello
import cv2
import matplotlib
import numpy as np
import math
import functions
from functions import *
from time import sleep
###############################################################################
# Main
###############################################################################

# continue taking pictures until a red, green, and blue center have been located
while True:
    print('\nFinding centers...')

    # Take a photo and correct its gamma
    #ref_img = gamma_correct_snap(1, 1)
    ref_img = snap(1)

    # Filter the colors we are looking for
    red_filtered = find_color('red', ref_img)
    green_filtered = find_color('green', ref_img)
    blue_filtered = find_color('blue', ref_img)

    # find the center points and get a photo of the rectangle
    red_center, red_rectangle= find_rect_center(red_filtered)
    green_center, green_rectangle = find_rect_center(green_filtered)
    blue_center, blue_rectangle = find_rect_center(blue_filtered)

    # check to see if we actually got coordinates and combine the photos of rectangles if we did
    print(f"red:{red_center}, blue: {blue_center}, green {green_center}")
    if red_center and green_center and blue_center:
        rectangles = combine_photos([red_rectangle, green_rectangle, blue_rectangle])
        cv2.imshow('rect', rectangles)
        cv2.waitKey(2)
        cv2.destroyAllWindows()
        break
    else:
        print('\nFailed to find all values')
        print(f'\nred: {red_center}\ngreen:{green_center}\nblue:{blue_center}')
        print('\nTrying again in 5 seconds')
        rectangles = combine_photos([red_rectangle, green_rectangle, blue_rectangle])
        cv2.imshow('rect', rectangles)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        sleep(5)

print(f"\n\nCenters Found \nRed Center: {red_center}\nBlue Center: {blue_center}\nGreen Center: {green_center}")

# find the mid_point
mid_point = find_mid_point(green_center, red_center)

# find red point relative to mid
red_rtm = move_origin(red_center, mid_point)
print(f"\nred relative to midpoint: {red_rtm}")

# find green point relative to mid
green_rtm = move_origin(green_center, mid_point)
print(f"\ngreen relative to midpoint: {green_rtm}")

# find blue point relative to mid
blue_rtm = move_origin(blue_center, mid_point)
print(f"\nblue relative to midpoint: {blue_rtm}")

# find the rotation of green and blue points relative to the mid of the drone
green_rotation = calculate_angle(green_rtm)
blue_rotation = calculate_angle(blue_rtm)
print(f"\nBlue rotation: {blue_rotation}\nGreen rotation: {green_rotation}")

# calculate the rotation the drone needs
rotation = blue_rotation - green_rotation
if rotation < -180:
    rotation += 360
elif rotation > 180:
    rotation -= 360

print(f"\nRotation: {rotation}")

# add the center to the rectangle pictures and show it
int_mid = (int(mid_point[0]), int(mid_point[1]))
cv2.circle(rectangles, int_mid, 3, [000, 255, 000], -1)
cv2.imshow('rectangles', rectangles)
cv2.waitKey(0)
