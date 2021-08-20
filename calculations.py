# Dr. Xiang, Patrick Woolard, and Wesley Cooke with Augusta University School of Computer and Cyber Sciences
# Tello Drone - Vision based Navigation Research
# calculations.py

import math


class Calculations:
    """
        A class to handle math formulas
    """

    def distance_formula(self, point1, point2):
        """
            Function to compute the distance between two points.

            Parameters:
                point1 (list): List in the form of [x,y]
                point2 (list): List in the form of [x,y]

            returns:
                distance (float): The distance between the two points in their respective unit
        """

        distance = math.sqrt(((point2[0] - point1[0]) ** 2) + ((point2[1] - point1[1]) ** 2))
        return distance

    def find_mid_point(self, point1, point2):
        """
            Function to find the midpoint of two points

            Parameters:
                point1 (list): List in the form of [x,y]
                point2 (list): List in the form of [x,y]

            returns:
                mid_point (list): List in the form of [x,y]
        """

        # x = (x1 + x2)/2 and y = (y1 + y2)/2
        x = (point1[0] + point2[0]) / 2
        y = (point1[1] + point2[1]) / 2
        mid_point = [x, y]
        return mid_point

    def move_origin(self, point, axis_point):
        """
            Parameters:
                point (list): List in the form of [x,y]
                axis_point (list): List in the form of [x,y],

            returns:
                point_rta (list): Point in the form of [x,y] relative to the axis_point
        """

        # axis_point is treated as [h,k]. It is the origin of the new axis
        # point p(x,y) relative to the new axis is thus described as p(x-h, y-k)

        point_rta = [(point[0] - axis_point[0]), (point[1] - axis_point[1])]
        return point_rta

    def calculate_angle(self, point):
        """
            Function to calculate an angle of rotation given a point [x,y]
            special arctan rules found here https://learnandlearn.com/python-programming/python-reference/how-to-find-inverse-tan-or-arc-tan-in-python
            Ensure that the point is relative to the proper mid point

            Parameters:
                point (list): List in the form of [x,y]

            returns:
                angle (float): The angle that the point is rotated
        """

        # because inverse tangent has limitations, we have to do a little bit of checking to get a proper angle.

        x = point[0]
        y = point[1] * -1

        angle = math.atan2(y, x) * (180 / math.pi)
        if angle < 0:
            angle = angle + 360

        return angle
