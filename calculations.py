import math
class Calculations:
    """
        A class to handle calculating values
    """


    def distance_formula(self, point1, point2):
        """
            Function to compute the distance between two points.
            Takes two arguments
            Point1 and Point2 and separate lists in the form of [x,y]
            returns distance
        """

        distance = math.sqrt(((point2[0] - point1[0]) ** 2) + ((point2[1] - point1[1]) ** 2))
        return distance


    def find_mid_point(self, point1, point2):
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


    def move_origin(self, point, axis_point):
        """
            Translates a point to a new point relative to an axis.
            Takes two arguments in the form of [x,y]
            returns a point [x,y] relative to the axis point [x, y]
        """

        # axis_point is treated as [h,k]. It is the origin of the new axis
        # point p(x,y) relative to the new axis is thus described as p(x-h, y-k)

        point_rta = [(point[0] - axis_point[0]), (point[1] - axis_point[1])]
        return point_rta


    def calculate_angle(self, point):
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
