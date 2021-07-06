# Vision Based Navigation Research
# Augusta University School of Computer and Cyber Sciences
# Date Started 5/14/21
###############################################################################

import cv2
import numpy as np
import math


###############################################################################
# Functions
###############################################################################


def snap(camera_index):
    """
        Connects to the camera to take a picture.
        Takes one argument, camera_index, that is the index of the desired camera.
        Returns a frame
    """

    # connect to the camera
    cam = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

    # grab the frame
    ret, frame = cam.read()

    # if it could grab the frame, it returns the grabbed frame
    if ret:
        return frame


def live_snap(camera_index):
    """
        Debugging function that displays the video feed of the camera
        Takes one argument, camera_index, that is the index of the desired camera
    """

    # connect to the camera
    cam = cv2.VideoCapture(camera_index)

    # create a loop to loop through frames
    while True:

        # grab the frame
        ret, frame = cam.read()

        # show the frame 
        cv2.imshow('live_frames', frame)

        # quit on q 
        if cv2.waitKey(1) == ord('q'):
            break

        # release the camera from the program control, and destroy all lingering windows being displayed
        cam.release()
        cv2.destroyAllWindows()


def find_color(color, img):
    """
        Function that will find a color in a image.
        Takes two arguments.
        color is the string color you want to find. 'red' 'green' or 'blue'
        img is the image you want to find the color in.
        Returns a filtered image showing only the desired color
    """

    # convert the image to an HSV color range 
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # dictionaries for both lower and upper masks of red, green, and blue colors in hsv color 
    # hsv is normally 360 degrees of colors, but cv2 only uses 180 degrees. Divide the 360 circle values by 2. 
    upper_masks = {
        'red': [185, 255, 255],
        'green': [90, 255, 255],
        'blue': [150, 255, 255],
    }

    lower_masks = {
        'red': [140, 50, 200],
        'green': [30, 50, 22],
        'blue': [80, 25, 200],
    }

    # define the range of color
    lower_mask = np.array(lower_masks[color])
    upper_mask = np.array(upper_masks[color])

    # create the mask that will lay over the original image
    mask = cv2.inRange(hsv, lower_mask, upper_mask)
    # return mask

    # combine the photos
    combined = cv2.bitwise_and(img, img, mask=mask)
    return combined


def is_contour_rectangle(c):
    """
        Function used to determine if a contour is a rectangle
        Takes the argument c for contour
        Returns a bool

        Code found at https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/
    """

    perimeter = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
    return len(approx) == 4


def find_rect_center(filtered):
    """
        Function that will find a colored rectangle in a filtered image and compute its center
        Takes one argument, filtered, that is the color filtered image
        Returns a list [x, y] and the image with only the rectangles
    """

    # convert the image to gray, blur it slightly, and threshold it 
    gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    # find the contours in the binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # create a mask for contours we want to ignore
    ignored_contours = np.ones(thresh.shape[:2], dtype='uint8') * 255

    # loop through contours and ignore ones smaller than 500 area and if they are not a rectangle
    for c in contours:
        if cv2.contourArea(c) < 10:
            cv2.drawContours(ignored_contours, [c], -1, 0, -1)
            continue
        if not is_contour_rectangle(c):
            cv2.drawContours(ignored_contours, [c], -1, 0, -1)

    # create an image with only good contours and refined the contours
    rectangles = cv2.bitwise_and(thresh, thresh, mask=ignored_contours)

    contours, hierarchy = cv2.findContours(rectangles, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rectangles = cv2.cvtColor(rectangles, cv2.COLOR_GRAY2BGR)

    # create a list to hold [x,y] 
    centers = []

    for c in contours:
        # calculates the 'image moment' for each contour
        m = cv2.moments(c)

        # calculates x and y values
        if m["m00"] != 0:
            center_x = int(m["m10"] / m["m00"])
            center_y = int(m["m01"] / m["m00"])
        else:
            center_x, center_y = 0, 0

        # draw the outline of the rectangle
        cv2.drawContours(rectangles, [c], -1, (0, 255, 0), 2)
        cv2.circle(rectangles, (center_x, center_y), 1, (0, 0, 255), -1)

        # append the centers to the list
        centers.append(center_x)
        centers.append(center_y)

    return centers, rectangles


def live_tracking(delay, camera_index):
    """
        Function to track the different points in real time
        Takes two arguments
        delay is the number of milliseconds between each update
        camera_index is the index of the desired camera used to track
        Tracks blue and green points.
        Green is the position of the drone
        Blue is the destination point
    """

    # connect to the camera
    cam = cv2.VideoCapture(camera_index)

    # start a loop for the frames
    while True:
        # grab the frame
        ret, img = cam.read()

        # find the blue and red in the pictures
        blue_filtered = find_color('blue', img)
        green_filtered = find_color('green', img)

        # find the coordinates of the rectangles for the blue and green points
        blue_coords, blue_rectangle = find_rect_center(blue_filtered)
        green_coords, green_rectangle = find_rect_center(green_filtered)

        # print the coordinates to the console and wait the desired number of milliseconds
        print(f"Blue Cords: {blue_coords}\n Green Cords: {green_coords}")
        cv2.waitKey(delay)

    cam.realease()
    cv2.destroyAllWindows()


def combine_photos(list):
    """
        Function to combine photots.
        Argument is the list of photos
    """
    dst = list[0]

    for i in range(len(list)):
        if i == 0:
            pass
        else:
            alpha = 1.0 / (i + 1)
            beta = 1.0 - alpha
            dst = cv2.addWeighted(list[i], alpha, dst, beta, 0.0)

    return dst


def distance_formula(point1, point2):
    """
        Function to compute the distance between two points.
        Takes two arguments
        Point1 and Point2 and separate lists in the form of [x,y]
        returns distance
    """

    distance = math.sqrt(((point2[0] - point1[0]) ** 2) + ((point2[1] - point1[1]) ** 2))
    return distance


def find_mid_point(point1, point2):
    """
        Function to find the midpoint of two points
        Takes two arguments
        point1 and point2 are a list in the form [x, y]
        Returns a list in the form of [x, y]
    """

    # x = (x1 + x2)/2 and y = (y1 + y2)/2
    x = (point1[0] + point2[0]) / 2
    y = (point1[1] + point2[1]) / 2
    mid_point = [x, y]
    return mid_point


def move_origin(point, axis_point):
    """
        Translates a point to a new point relative to an axis.
        Takes two arguments in the form of [x,y]
        returns a point [x,y] relative to the axis point [x, y]
    """

    # axis_point is treated as [h,k]. It is the origin of the new axis
    # point p(x,y) relative to the new axis is thus described as p(x-h, y-k)

    point_rta = [(point[0] - axis_point[0]), (point[1] - axis_point[1])]
    return point_rta


def calculate_angle(point):
    """
        Function to calculate an angle of rotation given a point [x,y]
        special arctan rules found here https://learnandlearn.com/python-programming/python-reference/how-to-find-inverse-tan-or-arc-tan-in-python
    """

    # because inverse tangent has limitations, we have to do a little bit of checking to get a proper angle.

    x = point[0]
    y = point[1] * -1

    angle = math.atan2(y, x) * (180 / math.pi)
    if angle < 0:
        angle = angle + 360

    return angle


def nothing(x):
    """
        A function needed for the use of cv2's trackbars
        Used as a call back function
    """
    pass


def test_mask_values(camera_index, color, gamma):
    """
        Function to test what hsv values are needed in a room.
        Takes the argument camera_index and string color you are looking for.
    """

    # connect to the camera
    cam = cv2.VideoCapture(camera_index)

    # make a list of bars needed
    bars = ['l_h_' + color, 'l_s_' + color, 'l_v_' + color,
            'u_h_' + color, 'u_s_' + color, 'u_v_' + color]

    # create the track bars
    win_name = color + '_track'
    cv2.namedWindow(win_name)
    cv2.createTrackbar(bars[0], win_name, 0, 179, nothing)
    cv2.createTrackbar(bars[1], win_name, 0, 255, nothing)
    cv2.createTrackbar(bars[2], win_name, 0, 255, nothing)
    cv2.createTrackbar(bars[3], win_name, 179, 179, nothing)
    cv2.createTrackbar(bars[4], win_name, 255, 255, nothing)
    cv2.createTrackbar(bars[5], win_name, 255, 255, nothing)

    # continue updating frames
    while True:
        ret, frame = cam.read()
        if ret:
            frame = gamma_trans(frame, gamma)

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lower_mask = np.array([cv2.getTrackbarPos(bars[0], win_name),
                                   cv2.getTrackbarPos(bars[1], win_name),
                                   cv2.getTrackbarPos(bars[2], win_name)])
            upper_mask = np.array([cv2.getTrackbarPos(bars[3], win_name),
                                   cv2.getTrackbarPos(bars[4], win_name),
                                   cv2.getTrackbarPos(bars[5], win_name)])

            mask = cv2.inRange(hsv, lower_mask, upper_mask)
            result = cv2.bitwise_and(frame, frame, mask=mask)

            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            combined = np.concatenate((mask, result), axis=1)
            cv2.imshow(win_name, combined)

            if cv2.waitKey(2) == ord('q'):
                dict_lower = {color+'_lower': [cv2.getTrackbarPos(bars[0], win_name),
                                      cv2.getTrackbarPos(bars[1], win_name),
                                      cv2.getTrackbarPos(bars[2], win_name)]}
                dict_upper = {color+'_upper': [cv2.getTrackbarPos(bars[3], win_name),
                                      cv2.getTrackbarPos(bars[4], win_name),
                                      cv2.getTrackbarPos(bars[5], win_name)]}
                cam.release()
                cv2.destroyAllWindows()
                return dict_lower, dict_upper


def gamma_trans(img, gamma):
    """
        A function to mimic adjusting camera exposure
        Takes the arguments image and gamma
    """

    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    return cv2.LUT(img, gamma_table)


def gamma_correct_snap(camera_index, gamma):
    img = snap(camera_index)
    gamma_img = gamma_trans(img, gamma)
    return gamma_img


def find_color_test(color, img, lower_dict, upper_dict):
    """
        Function that will find a color in a image.
        Takes two arguments.
        color is the string color you want to find. 'red' 'green' or 'blue'
        img is the image you want to find the color in.
        Returns a filtered image showing only the desired color
    """

    # convert the image to an HSV color range
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define the range of color
    lower_mask = np.array(lower_dict[color + '_lower'])
    upper_mask = np.array(upper_dict[color + '_upper'])

    # create the mask that will lay over the original image
    mask = cv2.inRange(hsv, lower_mask, upper_mask)
    # return mask

    # combine the photos
    combined = cv2.bitwise_and(img, img, mask=mask)
    return combined