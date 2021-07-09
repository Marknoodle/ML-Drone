import cv2
from camera import ImgProcessing
from calculations import Calculations
from time import sleep
# Instantiate the class and ensure a good ref_image

processing = ImgProcessing(0)

while True:
    print("\nHere is the image to be processed...")
    cv2.imshow('ref_img', processing.ref_image)
    cv2.waitKey(2000)

    # Filter Colors using masks passed
    red_filtered = processing.find_color('red', [155, 120, 87], [179, 255, 255])
    green_filtered = processing.find_color('green', [56, 56, 79], [92, 255, 255])
    blue_filtered = processing.find_color('blue', [100, 77, 99], [123, 255, 158])

    # Find the rectangles
    red_rectangle = processing.find_rects(red_filtered)
    green_rectangle = processing.find_rects(green_filtered)
    blue_rectangle = processing.find_rects(blue_filtered)

    # find the centers and draw the contour onto the rectangle
    red_center, red_rect = processing.find_rects_center(red_rectangle)
    green_center, green_rect = processing.find_rects_center(green_rectangle)
    blue_center, blue_rect = processing.find_rects_center(blue_rectangle)

    print('\nHere are the centers we found...')
    print(f"\nred_center: {red_center}\ngreen_center: {green_center}\nblue_center: {blue_center}")
    if red_center and green_center and blue_center:
        print('\nGot all the centers!')
        break
    else:
        print('\nDid not find all centers')
        print("\nGetting new image...")
        processing.ref_image = processing.get_ref_image()
        print("\nGot new image...")



# make a picture with all rectangles
rects = [red_rect, green_rect, blue_rect]
combined_rects = processing.combine_photos(rects)

# instantiate our calculator
calculator = Calculations()

# find the drone midpoint
drone_mid_point = calculator.find_mid_point(red_center[0], green_center[0])

# find other points relative to the drone mid point
red_rtm = calculator.move_origin(red_center[0], drone_mid_point)
blue_rtm = calculator.move_origin(blue_center[0], drone_mid_point)
green_rtm = calculator.move_origin(green_center[0], drone_mid_point)

# find the green and blue rotation
green_rotation = calculator.calculate_angle(green_rtm)
blue_rotation = calculator.calculate_angle(blue_rtm)

# find the rotation the drone needs to take
drone_rotation = blue_rotation - green_rotation

if drone_rotation < -180:
    drone_rotation += 360
elif drone_rotation > 180:
    drone_rotation -= 360

# print all the cool stuff
print(f"\n Drone Mid Point: {drone_mid_point}")
print(f"\n red_rtm: {red_rtm}\n blue_rtm: {blue_rtm}\n green_rtm: {green_rtm}")
print(f"\n green rotation: {green_rotation}\n blue rotation: {blue_rotation}")
print(f"\ndrone rotation: {drone_rotation}")

# add the drone mid point to the rectangle picture
int_mid = (int(drone_mid_point[0]), int(drone_mid_point[1]))
cv2.circle(combined_rects, int_mid, 3, [000, 000, 255], -1)
cv2.imshow('rectangles', combined_rects)
cv2.waitKey(0)

# print(f"red {red_center}\n green {green_center}\n blue {blue_center}")

