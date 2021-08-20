# Dr. Xiang, Patrick Woolard, and Wesley Cooke with Augusta University School of Computer and Cyber Sciences
# Tello Drone - Vision based Navigation Research
# live_stream.py

import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from camera import ImgProcessing
from calculations import Calculations
from djitellopy import Tello


def live_stream(update_delay, tello_o):
    """
    Function made to run in a thread. It will constantly update the drones mid point and height, and plot these values

    Args:
        update_delay: how long to wait before checking the mid point again
        tello_o: the tello object

    Returns:
        mid_points_list: List of the mid points
    """
    # Connect to the camera
    live_processing = ImgProcessing(1)
    live_processing.set_ref_gamma(3)
    calculator = Calculations()

    # set the color range for the front of the drone -- green
    lower_front_mask = [46, 53, 53]
    upper_front_mask = [79, 255, 255]
    drone_front_color = 'green'

    # set the color range for the back of the drone -- blue
    lower_back_mask = [70, 25, 166]
    upper_back_mask = [112, 255, 255]
    drone_back_color = 'blue'

    plt.title('A Basic Line Plot')  # Title of the plot
    plt.xlabel('X-axis')  # X-Label
    plt.ylabel('Y-axis')  # Y-Label
    plt.ion()
    plt.show()

    x_drone = []
    y_drone = []
    drone_mid_points = []
    while True:
        # update the ref_image of our camera object
        live_processing.ref_image = live_processing.get_ref_image()
        live_processing.set_ref_gamma(3)
        while True:
            # Find the blue and green color
            front_filtered = live_processing.find_color(drone_front_color, lower_front_mask, upper_front_mask)
            back_filtered = live_processing.find_color(drone_back_color, lower_back_mask, upper_back_mask)

            # Find the blue and green contours
            front_conts = live_processing.find_good_contours(front_filtered, discarded_area=10)
            back_conts = live_processing.find_good_contours(back_filtered, discarded_area=20)

            # Find the center of the contours
            front_centers, front_conts = live_processing.find_contours_center(front_conts)
            back_centers, back_conts = live_processing.find_contours_center(back_conts)

            # If we have the centers, break out of the while loop
            if front_centers and back_centers:
                break
            # If we press the q key, give us time to save the graph and then break
            elif cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyWindow('test')
                plt.pause(30)
                break
            # If we did not have the center update the ref_image of our camera object
            else:
                live_processing.ref_image = live_processing.get_ref_image()
                live_processing.set_ref_gamma(3)

        # We have the centers if we make it this far so calculate the mid point
        drone_mid_point = calculator.find_mid_point(back_centers[0], front_centers[0])

        # Add the mid point to the mid points list and then break off the x and y values into separate lists for
        # matplotlib
        drone_mid_points.append(drone_mid_point)
        x_drone.append(drone_mid_point[0])
        y_drone.append(drone_mid_point[1] * -1) # multiply by -1 because the camera y-axis is inverted

        # display the ref_image
        cv2.imshow('test', live_processing.ref_image)

        # plot the graph of all the values
        plt.plot(x_drone, y_drone)
        plt.show()
        plt.pause(0.01)

        # reset the centers to be empty
        front_centers = []
        back_centers = []

        # if we press q, give us time to save the graph and return the mid point list
        if cv2.waitKey(update_delay) & 0xFF == ord('q'):
            cv2.destroyWindow('test')
            plt.pause(30)
            return drone_mid_points

