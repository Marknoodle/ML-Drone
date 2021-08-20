from camera import ImgProcessing
from calculations import Calculations
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as image
from djitellopy import Tello
from random import randint
from mpl_toolkits.mplot3d import Axes3D


def live_stream(update_delay, tello_o):

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

    fig = plt.figure(figsize = (8, 6), dpi=90)
    # Making 3D Plot using plot3D()
    ax = plt.axes(projection = '3d')

    # Setting Axis labels
    ax.set_xlabel('X-Axis')
    ax.set_ylabel('Y-Axis')
    ax.set_zlabel('Z-Axis')
    # ax.set_xlim(0,1920)
    # ax.set_ylim()
    img = image.imread('drone_pic.png')

    plt.ion()
    plt.show()

    x_drone = []
    y_drone = []
    z_drone = []
    drone_mid_points = []
    while True:
        live_processing.ref_image = live_processing.get_ref_image()
        live_processing.set_ref_gamma(3)
        while True:
            front_filtered = live_processing.find_color(drone_front_color, lower_front_mask, upper_front_mask)
            back_filtered = live_processing.find_color(drone_back_color, lower_back_mask, upper_back_mask)

            front_conts = live_processing.find_good_contours(front_filtered, discarded_area=10)
            back_conts = live_processing.find_good_contours(back_filtered, discarded_area=20)

            front_centers, front_conts = live_processing.find_contours_center(front_conts)
            back_centers, back_conts = live_processing.find_contours_center(back_conts)

            if front_centers and back_centers:
                break
            elif cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyWindow('test')
                plt.pause(30)
                break
            else:
                live_processing.ref_image = live_processing.get_ref_image()
                live_processing.set_ref_gamma(3)

        drone_mid_point = calculator.find_mid_point(back_centers[0], front_centers[0])

        drone_mid_points.append(drone_mid_point)
        x_drone.append(drone_mid_point[0])
        y_drone.append(drone_mid_point[1] * -1)
        z_drone.append(1) #

        cv2.imshow('live_trajectory', live_processing.ref_image)

        fig.figimage(img, x_drone[-1], y_drone[-1])
        ax.plot3D(x_drone, y_drone, z_drone)
        plt.show()
        plt.pause(0.01)

        front_centers = []
        back_centers = []

        if cv2.waitKey(update_delay) & 0xFF == ord('q'):
            cv2.destroyWindow('test')
            plt.pause(30)
            return drone_mid_points, x_drone, y_drone


if __name__ == '__main__':
    #tello = Tello()
    drone_mid_points, x_drone, y_drone = live_stream(1, 'tello')
