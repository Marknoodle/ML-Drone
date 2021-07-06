import cv2
import numpy as np
from time import sleep

class ImgProcessing:
    """
        Class to process images picked up with a usb webcam.
        Uses OpenCV to initialize connections to a webcam and do image processing.

        Attributes:
            ref_image (array) = Image used for processing
    """

    def __init__(self, camera_index):
        """
            Initialize the settings for the camera

            Parameters:
                camera_index (int): The camera index of the webcam to be used
        """
        self.cam = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        self.ref_image = self.get_ref_image()

    def get_ref_image(self):
        """
            Function to take a picture using the usb webcam.

            Returns:
                frame: A image captured from the webcam
        """
        x = 0
        while True:
            sleep(2)
            ret, frame = self.cam.read()
            if x == 2:
                return frame
            else:
                x += 1


    def find_color(self, color, lower_mask=None, upper_mask=None):
        """
            Function to find a color in a self.ref_image. Red, green, or blue.
            Default values for lower_mask:
            'red': [140, 50, 200], 'green': [30, 50, 22], and 'blue': [80, 25, 200].
            Default values for upper_mask:
            'red': [185, 255, 255], 'green': [90, 255, 255], and 'blue': [150, 255, 255].

            Parameters:
                color (string): The target color as a string
                lower_mask (list): The lower list for the mask of the target color in HSV color space
                upper_mask (list): The upper list for the mask of the target color in HSV color space

            Returns:
                filtered (array): A image that has isolated the target color
        """

        # Define lower and upper mask if no list is passed
        if lower_mask is None:
            lower = {
                'red': [140, 50, 200],
                'green': [30, 50, 22],
                'blue': [80, 25, 200],
            }
            lower_mask = np.array(lower[color])
        else:
            lower_mask = np.array(lower_mask)

        if upper_mask is None:
            upper = {
                'red': [185, 255, 255],
                'green': [90, 255, 255],
                'blue': [150, 255, 255],
            }
            upper_mask = np.array(upper[color])
        else:
            upper_mask = np.array(upper_mask)

        # Convert the image to hsv, apply a mask using the lower and upper values, and transfer the image back to color
        hsv_img = cv2.cvtColor(self.ref_image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_img, lower_mask, upper_mask)
        filtered = cv2.bitwise_and(self.ref_image, self.ref_image, mask=mask)

        return filtered

    def has_four_corners(self, contour):
        """
            Function to determine if a contour has 4 corners

            Parameters:
                contour (array): The contour in question

            Returns:
                has_four (bool): A boolean value that states whether the contour has approximately 4 corners
        """
        # find the perimeter of the contours
        perimeter = cv2.arcLength(contour, True)
        # approximate the corners
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        has_four = len(approx) == 4
        return has_four

    def find_rects(self, filtered):
        """
            Function to find rectangles in an image that has been color filtered.

            Parameters:
                 filtered (array): An image that has been colored filtered.

            Returns:
                rectangles (array): A binary image with only rectangles present
        """

        gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

        # find the contours in the binary image
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # create a mask for contours we want to ignore
        ignored_contours = np.ones(thresh.shape[:2], dtype='uint8') * 255

        # loop through contours and ignore ones smaller than 10 area and if they are not a rectangle
        for c in contours:
            if cv2.contourArea(c) < 20:
                cv2.drawContours(ignored_contours, [c], -1, 0, -1)
                continue
            # if not self.has_four_corners(c):
            #     cv2.drawContours(ignored_contours, [c], -1, 0, -1)

        # create an image with only rectangle contours
        rectangles = cv2.bitwise_and(thresh, thresh, mask=ignored_contours)
        return rectangles

    def find_rects_center(self, rectangles):
        """
            Function to find the center of rectangles in an image

            Parameters:
                rectangles (array): Image that has been color filtered and rectangle filtered

            Returns:
                centers (list): A list containing lists of [x,y] coordinates. ie-> [[x,y],[x,y],[x,y]] or [[x,y]]
                rectangles (array): The binary rectangles image with colored colored centers and contours.
        """
        # Find the contour. There should only be rectangles left at this point in the processing stage
        contours, hierarchy = cv2.findContours(rectangles, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rectangles = cv2.cvtColor(rectangles, cv2.COLOR_GRAY2BGR)

        # Create a list to hold the lists of coordinates of the centers [x,y]
        centers = []

        for c in contours:
            # use an empty list to hold the center
            center = []

            # calculates the 'image moment' for each contour
            m = cv2.moments(c)

            # calculates x and y values
            if m["m00"] != 0:
                center_x = int(m["m10"] / m["m00"])
                center_y = int(m["m01"] / m["m00"])
            else:
                center_x, center_y = 0, 0

            # draw the contour and center of the rectangle
            cv2.drawContours(rectangles, [c], -1, (0, 255, 0), 2)
            cv2.circle(rectangles, (center_x, center_y), 1, (0, 0, 255), -1)

            # update the center list and append them to the centers list
            center.append(center_x)
            center.append(center_y)
            centers.append(center)

        return centers, rectangles

    def combine_photos(self, list):
        """
            Function to overlay photos on each other

            Parameters:
                list (list): A list of the photos you want combined

            Returns:
                img (array): an image of the photos overlayed on each other
        """

        img = list[0]
        for i in range(len(list)):
            if i == 0:
                pass
            else:
                alpha = 1.0 / (i + 1)
                beta = 1.0 - alpha
                img = cv2.addWeighted(list[i], alpha, img, beta, 0.0)

        return img

    def get_mask_values(self, window_name):
        """
            Function to test mask values for different colors

            Parameters:
                window_name (string): The name of the window. Ideally the color you are testing for

            Returns:
                lower_mask (numpy.array): A list of the lower mask values in HSV color space. [0-179, 0-255, 0-255]
                upper_mask (numpy.array): A list of the upper mask values in HSV color space. [0-179, 0-255, 0-255]
        """

        # create an empty callback function to use with OpenCV's trackbars
        def trackbar_pass(x):
            pass

        # create a window for all the track bars and initialize the trackbars
        cv2.namedWindow(window_name)
        cv2.createTrackbar('l_h', window_name, 0, 179, trackbar_pass)
        cv2.createTrackbar('l_s', window_name, 0, 255, trackbar_pass)
        cv2.createTrackbar('l_v', window_name, 0, 255, trackbar_pass)
        cv2.createTrackbar('u_h', window_name, 179, 179, trackbar_pass)
        cv2.createTrackbar('u-s', window_name, 255, 255, trackbar_pass)
        cv2.createTrackbar('u-v', window_name, 255, 255, trackbar_pass)

        # continue updating frames
        while True:
            ret, frame = self.cam.read()
            if ret:
                # make the picture hsv
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                # define the masks based on the trackbar positions
                lower_mask = np.array([cv2.getTrackbarPos('l_h', window_name),
                                       cv2.getTrackbarPos('l_s', window_name),
                                       cv2.getTrackbarPos('l_v', window_name)])

                upper_mask = np.array([cv2.getTrackbarPos('u_h', window_name),
                                       cv2.getTrackbarPos('u-s', window_name),
                                       cv2.getTrackbarPos('u-v', window_name)])

                # apply the mask to the hsv and overlay it on the original image
                mask = cv2.inRange(hsv, lower_mask, upper_mask)
                result = cv2.bitwise_and(frame, frame, mask=mask)

                # To place both pictures side by side, cv2 will not accept the binary mask,
                # so instead we convert it to gray, and then it works
                mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
                combined = np.concatenate((mask, result), axis=1)
                # Show both images, side by side
                cv2.imshow(window_name, combined)

                # Code to exit on 'q' for quit or 'n' for next: common keys
                if cv2.waitKey(2) == ord('q') or cv2.waitKey(2) == ord('n'):
                    # destroy the interface and return the trackbar values
                    cv2.destroyAllWindows()
                    return lower_mask, upper_mask

    def set_img_gamma(self, gamma):
        """
            Function that changes the gamma of the ref_img

            Parameters:
                gamma (int): The value of gamma you want

            Returns:
                img (array): gamma corrected img
        """

        gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
        gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
        return cv2.LUT(self.ref_image, gamma_table)
