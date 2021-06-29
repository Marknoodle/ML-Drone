import cv2
import numpy as np


class ImgProcessing:
    """
        Class to process images picked up with a usb webcam.
        Uses OpenCV to initialize connections to a webcam and do image processing.

        Attributes:
            camera_index (int): The camera index of the webcam to be used
    """

    def __init__(self, camera_index):
        """
            Initialize the settings for the camera

            Parameters:
                camera_index (int): The camera index of the webcam to be used
        """
        self.cam = cv2.VideoCapture(camera_index)

    def snap(self):
        """
            Function to take a picture using the usb webcam.

            Returns:
                frame: A image captured from the webcam
        """
        ret, frame = self.cam.read()

        if ret:
            return frame

    def find_color(self, color, ref_image=None, lower_mask=None, upper_mask=None):
        """
            Function to find a color in a specified image. Red, green, or blue.
            Function will snap a picture if one is not passed
            Default values for lower_mask:
            'red': [140, 50, 200], 'green': [30, 50, 22], and 'blue': [80, 25, 200].
            Default values for upper_mask:
            'red': [185, 255, 255], 'green': [90, 255, 255], and 'blue': [150, 255, 255].

            Parameters:
                color (string): The target color as a string
                ref_image (array): The image you want to find the color in
                lower_mask (list): The lower list for the mask of the target color in HSV color space
                upper_mask (list): The upper list for the mask of the target color in HSV color space

            Returns:
                filtered (array): A image that has isolated the target color
        """

        # Take a picture to filter if none is passed
        if ref_image is None:
            ref_image = self.snap()

        # Define lower and upper mask if no list is passed
        if lower_mask is None:
            lower = {
                'red': [140, 50, 200],
                'green': [30, 50, 22],
                'blue': [80, 25, 200],
            }
            lower_mask = lower[color]

        if upper_mask is None:
            upper = {
                'red': [185, 255, 255],
                'green': [90, 255, 255],
                'blue': [150, 255, 255],
            }
            upper_mask = upper[color]

        # Convert the image to hsv, apply a mask using the lower and upper values, and transfer the image back to color
        hsv_img = cv2.cvtColor(ref_image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_img, lower_mask, upper_mask)
        filtered = cv2.bitwise_and(ref_image, ref_image, mask=mask)

        return filtered

    def has_four_corners(self, contour):
        """
            Function to determine if a contour has 4 corners

            Parameters:
                contour (array): The contour in question

            Returns:
                has_four (bool): A boolean value that states whether the contour has approximately 4 corners
        """

        perimeter = cv2.arcLenth(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        has_four = len(approx) == 4
        return has_four

    def find_rects(self, filtered):
        """
            Function to find rectangles in an image that has been color filtered.

            Parameters:
                 filtered (array): An image that has been colored filtered.

            Returns:
                rectangles (array): An image with only the rectangles in the filtered image
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
            if cv2.contourArea(c) < 10:
                cv2.drawContours(ignored_contours, [c], -1, 0, -1)
                continue
            if not self.has_four_corners(c):
                cv2.drawContours(ignored_contours, [c], -1, 0, -1)

        # create an image with only rectangle contours
        rectangles = cv2.bitwise_and(thresh, thresh, mask=ignored_contours)
        return rectangles

    def find_rects_center(self, rectangles):
        """
            Function to find the center of rectangles in an image

            Parameters:
                rectangles (array): Image that has been color filtered and rectangle filtered

            Returns:
                centers (list): A list containing other lists of [x,y] coordinates.
                rectangles (array): The original image with its contours and centers drawn
        """
        # Find the contour. There should only be rectangles left at this point in the processing stage
        contours, hierarchy = cv2.findContours(rectangles, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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
            center = [center_x, center_y]
            centers.append(center)

        return centers, rectangles

    def combine_photos(self, list):
        """
            Function to overlay photos on each other

            Parameters:
                list (list): A list of the photos you want combined

            Returns:
                overlayed (array): an image of the photos overlayed on each other
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
