import cv2
from camera import ImgProcessing
from calculations import Calculations

# initialize camera and calculator
processing = ImgProcessing(1)
processing.set_ref_gamma(3)
calculator = Calculations()

# define masks for color filtering
lower_red_mask = [172, 99, 10]
upper_red_mask = [179, 254, 255]

lower_green_mask = [46, 53, 53]
upper_green_mask = [79, 255, 255]

lower_blue_mask = [80, 25, 166]
upper_blue_mask = [101, 255, 255]

# Find destination points -- red points
while True:
    print("Here is the image used to find the destination points...\n")
    cv2.imshow('ref_img', processing.ref_image)
    cv2.waitKey(1000)

    # find the red points
    red_filtered = processing.find_color('red', lower_red_mask, upper_red_mask)
    red_conts = processing.find_good_contours(red_filtered)
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
        processing.get_ref_image()
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

for destination in destinations:
    # Find the drone -- blue and green point
    while True:
        print('Here is the image used to find the drone\n')
        cv2.imshow('ref_img', processing.ref_image)
        cv2.waitKey(1000)

        green_filtered = processing.find_color('green', lower_green_mask, upper_green_mask)
        blue_filtered = processing.find_color('blue', lower_blue_mask, upper_blue_mask)

        green_conts = processing.find_good_contours(green_filtered)
        blue_conts = processing.find_good_contours(blue_filtered)

        green_centers, green_conts = processing.find_contours_center(green_conts)
        blue_centers, blue_conts = processing.find_contours_center(blue_conts)

        print(f'The green center is: {green_centers}\nThe blue center is {blue_centers}')

        if green_centers and blue_centers:
            print('Found the drone!\n\n')
            break
        else:
            print('Did not find the drone...\n')
            print('Getting new img...\n')
            processing.get_ref_image()
            processing.set_ref_gamma(3)
            print('Got new img...\n')

    # make a picture with all the conts
    conts = [red_conts, blue_conts, green_conts]
    conts_combined = processing.combine_photos(conts)

    # find the drone midpoint -> The distance between green and blue points
    drone_mid_point = calculator.find_mid_point(blue_centers, green_centers)









#only grab