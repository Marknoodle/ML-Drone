import cv2
from camera import ImgProcessing
from calculations import Calculations
from djitellopy import Tello
from time import sleep

# Instantiate the class and ensure a good ref_image
processing = ImgProcessing(1)
processing.set_ref_gamma(3)

# Do all the image processing and get the centers
while True:
    print("\nHere is the image to be processed...")
    cv2.imshow('ref_img', processing.ref_image)
    cv2.waitKey(1000)

    # Filter Colors using masks passed gcc colors
    # red_filtered = processing.find_color('red', [172, 99, 10], [179, 254, 255])
    # green_filtered = processing.find_color('green', [46, 53, 53], [79, 255, 255])
    # blue_filtered = processing.find_color('blue', [80, 25, 166], [101, 255, 255])

    # Filter Colors using masks passed home colors
    red_filtered = processing.find_color('red', [172, 99, 10], [179, 254, 255])
    green_filtered = processing.find_color('green', [46, 53, 53], [79, 255, 255])
    blue_filtered = processing.find_color('blue', [80, 25, 166], [101, 255, 255])

    # Find the good contours
    red_conts = processing.find_good_contours(red_filtered)
    green_conts = processing.find_good_contours(green_filtered)
    blue_conts = processing.find_good_contours(blue_filtered)

    # find the centers and draw the contours
    red_centers, red_conts = processing.find_contours_center(red_conts)
    green_centers, green_conts = processing.find_contours_center(green_conts)
    blue_centers, blue_conts = processing.find_contours_center(blue_conts)

    print('\nHere are the centers we found...')
    print(f"\nred_center: {red_centers}\ngreen_center: {green_centers}\nblue_center: {blue_centers}")
    if red_centers and green_centers and blue_centers:
        print('\nGot all the centers!')
        break
    else:
        print('\nDid not find all centers')
        print("\nGetting new image...")
        processing.ref_image = processing.get_ref_image()
        print("\nGot new image...")

# make a picture with all rectangles
conts = [red_conts, green_conts, blue_conts]
conts_combined = processing.combine_photos(conts)

# instantiate our calculator class
calculator = Calculations()

# find the drone midpoint -> The distance between green and blue points
drone_mid_point = calculator.find_mid_point(blue_centers[0], green_centers[0])

# find other points relative to the drone mid point
red_rtm = calculator.move_origin(red_centers[0], drone_mid_point)
blue_rtm = calculator.move_origin(blue_centers[0], drone_mid_point)
green_rtm = calculator.move_origin(green_centers[0], drone_mid_point)

# find the green and red rotation
# green rotation is the direction the drone is facing
# red rotation is the angle of the destination point
green_rotation = calculator.calculate_angle(green_rtm)
red_rotation = calculator.calculate_angle(red_rtm)

# find the rotation the drone needs to take
drone_rotation = red_rotation - green_rotation

# calculate the pixel distance and then multiply by a fraction to turn into cm distance
mid_to_des = calculator.distance_formula(red_rtm, drone_mid_point) * 100/400

if drone_rotation < -180:
    drone_rotation += 360
elif drone_rotation > 180:
    drone_rotation -= 360

# print all the cool stuff
print(f"\n Drone Mid Point: {drone_mid_point}")
print(f"\n red_rtm: {red_rtm}\n blue_rtm: {blue_rtm}\n green_rtm: {green_rtm}")
print(f"\n green rotation: {green_rotation}\n red rotation: {red_rotation}")
print(f"\ndrone rotation: {drone_rotation}")
print(f"")

# add the drone mid point to the rectangle picture
int_mid = (int(drone_mid_point[0]), int(drone_mid_point[1]))
cv2.circle(conts_combined, int_mid, 1, [000, 000, 255], -1)
cv2.imshow('rectangles', conts_combined)
cv2.waitKey(0)
cv2.destroyAllWindows()

# delay = 2
# tello = Tello()
# sleep(delay)
#
# tello.connect()
# sleep(delay)
#
# tello.set_speed(10)
# sleep(delay)
#
# tello.takeoff()
# sleep(delay)
#
# tello.rotate_counter_clockwise(int(drone_rotation))
# sleep(delay)
#
# tello.move_forward(int(mid_to_des))
# sleep(delay)
#
# tello.land()






