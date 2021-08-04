# Dr. Xiang, Patrick Woolard, and Wesley Cooke with Augusta University School of Computer and Cyber Sciences
# Tello Drone - Vision based Navigation Research
# test_mask.py

import cv2
from camera import ImgProcessing

# File to test for masks values

# Initialize the camera with the proper camera index
processing = ImgProcessing(1)
gamma = 3
# Use the Trackbar function to test the mask values for lower color and upper colors
lr, ur = processing.get_mask_values('red', gamma)
lg, ug = processing.get_mask_values('green', gamma)
lb, ub = processing.get_mask_values('blue', gamma)

# Test the masks using our color filtering function
red_filtered = processing.find_color('red', lr, ur)
green_filtered = processing.find_color('green', lg, ug)
blue_filtered = processing.find_color('blue', lb, ub)

# Print what the values we set are
print(f"lr: {lr}, ur:{ur}\n")
print(f"lg: {lg}, ug:{ug}\n")
print(f"lb: {lb}, ub:{ub}\n")

# Show the results of testing the color filtering with the masks we chose
cv2.imshow('red', red_filtered)
cv2.imshow('green', green_filtered)
cv2.imshow('blue', blue_filtered)
cv2.waitKey(0)
