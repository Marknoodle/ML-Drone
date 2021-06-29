# Vision Based Navigation Research
# Augusta University School of Computer and Cyber Sciences
# Date Started 5/14/21
###############################################################################

from djitellopy import Tello
from time import sleep
import cv2
import matplotlib
import numpy as np
import math

###############################################################################
# Functions
###############################################################################

def snap():
    # Function to take a picture

    # Connect to camera, take a picture, and release camera
    cam = cv2.VideoCapture(1)

    ret, frame = cam.read()
    cam.release()

    # Return the picture
    if ret:
        return frame


    
def live_snap():
    # Function to show what the camera is seeing
    cam = cv2.VideoCapture(1)

    while(True):
        ret, frame = cam.read()

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

def filter_blue(img):
    # Function to isolate blue color 

    # Convert the image to an HSV color range
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the range of blue using Hue Saturation Value
    # Cv2 only uses 0-180 for hue so divide the 360 circle value by 2. 
    lower_blue = np.array([80,25,200])
    upper_blue = np.array([150, 255, 255])

    # Mask that will lay over the original image
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Combine the photos 
    #result = cv2.bitwise_and(img, img, mask = mask)

    return mask

def filter_red(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = np.array([140,50,200])
    upper_red = np.array([185, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    #result = cv2.bitwise_and(img, img, mask = mask)
    return mask 

def filter_green(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green = np.array([30,50,100])
    upper_green = np.array([90, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)

    #result = cv2.bitwise_and(img, img, mask = mask)
    return mask 

def is_countour_bad(c):
    # Function that checks if a countour is a rectangle 

    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    return not len(approx) == 4

def find_center(mask):
    
    blurred = cv2.GaussianBlur(mask, (5,5), 0)

    #coonvert the grey image to binary image and threshold it
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    
    # Debugging 
    #cv2.imshow('thresh', thresh)
    #

    #find countours in the binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a mask for the bad contours
    bad_countours = np.ones(thresh.shape[:2], dtype="uint8") * 255

    for c in contours:
        if cv2.contourArea(c) < 500:
            cv2.drawContours(bad_countours, [c], -1, 0, -1)
            continue
        if is_countour_bad(c):
            cv2.drawContours(bad_countours, [c], -1, 0, -1)
    
    #Debugging
    #cv2.imshow('bad', bad_countours)
    #

    rectangles = cv2.bitwise_and(thresh, thresh, mask = bad_countours)
    #Debugging
    #cv2.imshow('rectangles', rectangles)
    #

    countours, hierarchy = cv2.findContours(rectangles, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    centers = []
    for c in countours: 
        #calculates moment for each countour
        M = cv2.moments(c)

        #calculate x,y coordinate of center
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else: 
            cX, cY = 0, 0
        cv2.drawContours(rectangles, [c], -1, (0,255,0), 2)
        cv2.circle(rectangles, (cX, cY), 1, (0, 0, 255), -1)

        centers.append(cX)
        centers.append(cY)
        #Debugging
        #print(f"{cX}, {cY}")
        #

    return centers, rectangles

def live_tracking(time):
    cam = cv2.VideoCapture(1)

    while True:
        ret, img = cam.read()
        mask = np.ones(img.shape[:2], dtype="uint8") * 255

        bluemask = filter_blue(img)
        greenmask = filter_green(img)

        bluecenter, bluerectangles = find_center(bluemask)
        greencenter, greenrectangles = find_center(greenmask)

        print(f" Blue centers: {bluecenter}, Green centeres: {greencenter}")
        cv2.imshow('Blue', bluerectangles)
        cv2.imshow('Green', greenrectangles)
        cv2.waitKey(time)

    cam.release()
    cv2.destroyAllWindows()

def find_centers():
    img = snap()

    blueimg = filter_blue(img)
    redimg = filter_red(img)
    greenimg = filter_green(img)

    #debugging 
    cv2.imshow('blueimg',blueimg)
    cv2.imshow('green', greenimg)
    cv2.imshow('red',redimg)
    cv2.waitKey(0)
    #

    bluecenter, blue = find_center(blueimg)
    redcenter, red = find_center(redimg)
    greencenter, green = find_center(greenimg)


    #test
    image_data = []
    image_data.append(blue)
    image_data.append(red)
    image_data.append(green)

    dst = image_data[0]
    for i in range(len(image_data)):
        if i == 0:
            pass
        else:
            alpha = 1.0/(i+1)
            beta = 1.0-alpha
            dst = cv2.addWeighted(image_data[i],alpha, dst, beta, 0.0)
    #

    return bluecenter, redcenter, greencenter, dst

def distance_formula(start, end):
    """ Computes the distance from two points
        Requires 
    """
    distance = math.sqrt( ((end[0] - start[0])**2) + ((end[1] - start[1])**2) ) 
    return distance 


###############################################################################
# Main
###############################################################################





bluecenter, redcenter, greencenter, rectangles = find_centers()

print(bluecenter)
print(redcenter)
print(greencenter)

green_to_blue = distance_formula(greencenter, bluecenter)
red_to_blue = distance_formula(redcenter, bluecenter)
red_to_green = distance_formula(redcenter,greencenter)

print(green_to_blue)
print(red_to_blue)
print(red_to_green)


cv2.imshow('rects', rectangles)
cv2.waitKey(0)

cv2.destroyAllWindows()


#tello = Tello()
#tello.connect()
#tello.set_speed(10)
#tello.takeoff()
#time.sleep(5)
##tello.move_forward(int(cmdistance))
#tello.land()


#live_tracking(1)












