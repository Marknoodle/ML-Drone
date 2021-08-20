import cv2
from time import sleep
from djitellopy import Tello
from camera import ImgProcessing
from calculations import Calculations
import numpy as np
import threading
from live_stream import live_stream

# define masks for red color filtering
# lower_red_mask = [172, 99, 10]
# upper_red_mask = [179, 254, 255]
#
# lower_green_mask = [46, 53, 53]
# upper_green_mask = [79, 255, 255]
#
# lower_blue_mask = [70, 25, 166]  # [ 70  25 166], ur:[112 255 255]
# upper_blue_mask = [112, 255, 255]

# # initialize Camera and calculator
processing = ImgProcessing(1)
processing.set_ref_gamma(3)
calculator = Calculations()
#
# initalize tello
# tello = Tello()
# tello.connect()
# tello.set_speed(25)
# sleep(2)

# Set the fraction to multiply by for converting from pixel distance to real world distance
pixel_to_real_fract = 100 / 192

# set the color range for the destination points -- white
lower_des_mask = [0, 0, 0]
upper_des_mask = [0, 0, 255]
des_color = 'white'

# set the color range for the front of the drone -- green
lower_front_mask = [46, 53, 53]
upper_front_mask = [79, 255, 255]
drone_front_color = 'green'

# set the color range for the back of the drone -- blue
lower_back_mask = [70, 25, 166]
upper_back_mask = [112, 255, 255]
drone_back_color = 'blue'

# Start a thread for recording and monitoring video

# recording_thread = threading.Thread(target=live_stream, args=[200, tello])
# recording_thread.start()

# Find destination points -- white_points
while True:
    print("Here is the image used to find the destination points...\n")
    cv2.imshow('ref_img', processing.ref_image)
    cv2.waitKey(1000)

    # find the destination points
    des_filtered = processing.find_color(des_color, lower_des_mask, upper_des_mask)
    des_conts = processing.find_good_contours(des_filtered, discarded_area=1000)
    des_centers, des_conts = processing.find_contours_center(des_conts)

    print(f'The destination points are {des_centers}')

    if des_centers:
        print('Located Destinations...')
        cv2.imshow('des_conts', des_conts)
        cv2.waitKey(5000)
        cv2.destroyWindow('ref_img')
        cv2.destroyWindow('des_conts')
        print('Looking for drone...\n')
        break
    else:
        print('Did not get any destination points...\nGetting a new img...')
        processing.ref_image = processing.get_ref_image()
        processing.set_ref_gamma(3)
        cv2.destroyWindow('ref_img')

"""
Instructions to find the drone
    For each destination:
        1. Locate the drone
        2. Find the midpoint of the drone
        3. Find all colored points relative to the midpoint of the drone
        4. Find the rotation of the destination and the front of the drone relative to the drone mid point
        5. Find the rotation the drone needs to take 
        6. Find the real distance from the drone mid point to the destination
        7. Fly the drone
"""

tello.takeoff()

counter = 1
mid_points_list = np.array([])
for destination in des_centers:
    # Find the drone
    while True:
        print('Here is the image used to find the drone')
        cv2.imshow('ref_img', processing.ref_image)
        cv2.waitKey(1000)

        front_filtered = processing.find_color(drone_front_color, lower_front_mask, upper_front_mask)
        back_filtered = processing.find_color(drone_back_color, lower_back_mask, upper_back_mask)

        front_conts = processing.find_good_contours(front_filtered, discarded_area=10)
        back_conts = processing.find_good_contours(back_filtered, discarded_area=20)

        front_centers, front_conts = processing.find_contours_center(front_conts)
        back_centers, back_conts = processing.find_contours_center(back_conts)

        print(f'The front of the drone is is: {front_centers}\nThe back of the drone is {back_centers}')

        if front_centers and back_centers:
            print('Located the drone!\n')
            cv2.destroyWindow('ref_img')
            break
        else:
            print('Did not find the drone...')
            print('Getting new img...')
            processing.ref_image = processing.get_ref_image()
            processing.set_ref_gamma(3)
            cv2.destroyWindow('ref_img')

    # After locating the drone, do the calculations

    # make a picture with all the conts
    conts = [des_conts, back_conts, front_conts]
    conts_combined = processing.combine_photos(conts)

    # find the drone midpoint -> The distance between front and back points
    # append the drone mid points to a list
    drone_mid_point = calculator.find_mid_point(back_centers[0], front_centers[0])
    mid_points_list = np.append(mid_points_list, drone_mid_point)

    # add the first point to the destinations so that we go back to it at the end
    if counter == 1:
        des_centers.append(drone_mid_point)
    counter += 1

    # find other points relative to the drone mid point
    destination_rtm = calculator.move_origin(destination, drone_mid_point)
    back_rtm = calculator.move_origin(back_centers[0], drone_mid_point)
    front_rtm = calculator.move_origin(front_centers[0], drone_mid_point)

    # find the destination and drone front rotations
    front_rotation = calculator.calculate_angle(front_rtm)
    destination_rotation = calculator.calculate_angle(destination_rtm)

    # find the rotation the drone needs to take to face the destination
    drone_rotation = destination_rotation - front_rotation

    if drone_rotation < -180:
        drone_rotation += 360
    elif drone_rotation > 180:
        drone_rotation -= 360

    # calculate the pixel distance and then multiply by a fraction to turn into cm distance
    mid_to_des = calculator.distance_formula(destination, drone_mid_point) * pixel_to_real_fract

    # print all the cool stuff
    print(f'Navigation to point: {destination}')
    print(f'Moving {mid_to_des}cm...')
    print(f"Drone Mid Point: {drone_mid_point}")
    print(f"Des_RTM: {destination_rtm}\nBack_RTM: {back_rtm}\nFront_RTM: {front_rtm}")
    print(f"Front of drone Rotation: {front_rotation}\nDestination rotation: {destination_rotation}")
    print(f"Drone rotation: {drone_rotation}")
    print(f"")

    # add the drone mid point to the rectangle picture
    int_mid = (int(drone_mid_point[0]), int(drone_mid_point[1]))
    cv2.circle(conts_combined, int_mid, 1, [000, 000, 255], -1)
    cv2.imshow('rectangles', conts_combined)
    cv2.waitKey(5000)
    cv2.destroyWindow('rectangles')

    # Tell the drone what to do
    tello.rotate_counter_clockwise(int(drone_rotation))
    sleep(2)
    tello.move_forward(int(mid_to_des))

    # get a new image
    processing.ref_image = processing.get_ref_image()
    processing.set_ref_gamma(3)

tello.land()

cv2.destroyAllWindows()
recording_thread.join()
processing.cam.release()
