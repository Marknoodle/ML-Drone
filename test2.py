# from calculations import Calculations
import cv2
from camera import ImgProcessing

processing = ImgProcessing(0)
# red_filtered = processing.find_color('red', [155, 120, 87], [179, 255, 255])
# green_filtered = processing.find_color('green', [56, 56, 79], [ 92, 255, 255])
# blue_filtered = processing.find_color('blue', [100, 77,  99], [123, 255, 158])
#
# # Find the rectangles
# red_rectangle = processing.find_rects(red_filtered)
# green_rectangle = processing.find_rects(green_filtered)
# blue_rectangle = processing.find_rects(blue_filtered)
#
# # find the centers and draw the contour onto the rectangle
# red_center, red_rect = processing.find_rects_center(red_rectangle)
# green_center, green_rect = processing.find_rects_center(green_rectangle)
# blue_center, blue_rect = processing.find_rects_center(blue_rectangle)
#
# print(f"\nred_center: {red_center}\ngreen_center: {green_center}\nblue_center: {blue_center}")
#
# cv2.imshow('red', red_filtered)
# cv2.imshow('green', green_filtered)
# cv2.imshow('blue', blue_filtered)
#
# cv2.imshow('red_rect', red_rect)
# cv2.imshow('green_rect', green_rect)
# cv2.imshow('blue_rect', blue_rect)
# cv2.waitKey(0)

##################
# Testing Mask Values
lr, ur = processing.get_mask_values('red')
lg, ug = processing.get_mask_values('green')
lb, ub = processing.get_mask_values('blue')

# # Mask Value color filtering
# red_filtered = processing.find_color('red', lr, ur)
# green_filtered = processing.find_color('green', lg, ug)
# blue_filtered = processing.find_color('blue', lb, ub)



# print(f"lr: {lr}, ur:{ur}\n")
# print(f"lg: {lg}, ug:{ug}\n")
# print(f"lb: {lb}, ub:{ub}\n")

# Default color filtering
# red_filtered = processing.find_color('red')
# green_filtered = processing.find_color('green')
# blue_filtered = processing.find_color('blue')



