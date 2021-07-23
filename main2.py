import cv2
from time import sleep
from djitellopy import Tello
from camera import ImgProcessing
from calculations import Calculations
import numpy as np

# initialize camera and calculator
processing = ImgProcessing(1)
processing.set_ref_gamma(3)
calculator = Calculations()

# lw[0 0 0], uw:[  0   0 255]
lower_red_mask = [0, 0, 0]
upper_red_mask = [0, 0, 255]

# define masks for color filtering
# lower_red_mask = [172, 99, 10]
# upper_red_mask = [179, 254, 255]

lower_green_mask = [46, 53, 53]
upper_green_mask = [79, 255, 255]

lower_blue_mask = [70, 25, 166]     # [ 70  25 166], ur:[112 255 255]
upper_blue_mask = [112, 255, 255]

# Find destination points -- red points
while True:
    print("Here is the image used to find the destination points...\n")
    cv2.imshow('ref_img', processing.ref_image)
    cv2.waitKey(1000)

    # find the red points
    red_filtered = processing.find_color('red', lower_red_mask, upper_red_mask)
    red_conts = processing.find_good_contours(red_filtered, discarded_area=1000)
    red_centers, red_conts = processing.find_contours_center(red_conts)

    print(f'The destination points are {red_centers}\n')

    if red_centers:
        cv2.imshow('red_conts', red_conts)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print('Got the destinations, continuing...\n\n')
        destinations = red_centers
        break
    else:
        print('Did not get any destination points...\n')
        print('Getting new img...\n')
        processing.ref_image = processing.get_ref_image()
        processing.set_ref_gamma(3)
        print('Got new image...\n')

"""
    For each destination:
        1. Locate the drone
        2. Find the midpoint of the drone
        3. Find the points relative to the midpoint of the drone
        4. Find the rotation of the destination and the drone rt drone mid point
        5. Find the rotation the drone needs to take 
        6. Find the real distance from the drone mid point to the destination
        7. Fly the drone
"""
tello = Tello()
tello.connect()
tello.set_speed(20)
tello.takeoff()

counter = 1
mid_points_list = np.array([])
for destination in destinations:
    # Find the drone -- blue and green point
    while True:
        print('Here is the image used to find the drone\n')
        cv2.imshow('ref_img', processing.ref_image)
        cv2.waitKey(1000)

        green_filtered = processing.find_color('green', lower_green_mask, upper_green_mask)
        blue_filtered = processing.find_color('blue', lower_blue_mask, upper_blue_mask)

        green_conts = processing.find_good_contours(green_filtered, discarded_area=10)
        blue_conts = processing.find_good_contours(blue_filtered, discarded_area=20)

        green_centers, green_conts = processing.find_contours_center(green_conts)
        blue_centers, blue_conts = processing.find_contours_center(blue_conts)

        print(f'The green center is: {green_centers}\nThe blue center is {blue_centers}')

        if green_centers and blue_centers:
            print('Found the drone!\n\n')
            break
        else:
            print('Did not find the drone...\n')
            print('Getting new img...\n')
            processing.ref_image = processing.get_ref_image()
            processing.set_ref_gamma(3)
            print('Got new img...\n')

    # make a picture with all the conts
    conts = [red_conts, blue_conts, green_conts]
    conts_combined = processing.combine_photos(conts)

    # find the drone midpoint -> The distance between green and blue points
    # append the drone mid points to a list
    drone_mid_point = calculator.find_mid_point(blue_centers[0], green_centers[0])
    mid_points_list = np.append(mid_points_list, drone_mid_point)

    # add the first point to the destinations so that we go back to it at the end
    if counter == 1:
        destinations.append(drone_mid_point)
    counter += 1

    # find other points relative to the drone mid point
    destination_rtm = calculator.move_origin(destination, drone_mid_point)
    blue_rtm = calculator.move_origin(blue_centers[0], drone_mid_point)
    green_rtm = calculator.move_origin(green_centers[0], drone_mid_point)

    # find the green and red rotation
    # green rotation is the direction the drone is facing
    # red rotation is the angle of the destination point
    green_rotation = calculator.calculate_angle(green_rtm)
    destination_rotation = calculator.calculate_angle(destination_rtm)

    # find the rotation the drone needs to take to face the destination
    drone_rotation = destination_rotation - green_rotation

    if drone_rotation < -180:
        drone_rotation += 360
    elif drone_rotation > 180:
        drone_rotation -= 360

    # calculate the pixel distance and then multiply by a fraction to turn into cm distance
    mid_to_des = calculator.distance_formula(destination, drone_mid_point) * 100 / 192

    # print all the cool stuff
    print(f'Navigation to point: {destination}\n')
    print(f'Moving {mid_to_des}cm...\n')
    print(f"\n Drone Mid Point: {drone_mid_point}")
    print(f"\n red_rtm: {destination_rtm}\n blue_rtm: {blue_rtm}\n green_rtm: {green_rtm}")
    print(f"\n green rotation: {green_rotation}\n red rotation: {destination_rotation}")
    print(f"\ndrone rotation: {drone_rotation}")
    print(f"")

    # add the drone mid point to the rectangle picture
    int_mid = (int(drone_mid_point[0]), int(drone_mid_point[1]))
    cv2.circle(conts_combined, int_mid, 1, [000, 000, 255], -1)
    cv2.imshow('rectangles', conts_combined)
    cv2.waitKey(2)
    cv2.destroyAllWindows()

    # Tell the drone what to do

    sleep(2)
    tello.rotate_counter_clockwise(int(drone_rotation))
    sleep(2)
    tello.move_forward(int(mid_to_des))


    # get a new image
    processing.ref_image = processing.get_ref_image()
    processing.set_ref_gamma(3)


tello.land()