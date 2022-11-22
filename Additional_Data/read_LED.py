from pytesseract import pytesseract
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import cv2
import pandas as pd
import os
import imutils
from os import listdir
#from imutils.perspective import four_point_transform
from imutils import contours

# define the dictionary of digit segments so we can identify
# each digit on the thermostat
DIGITS_LOOKUP = {
	(1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 1, 0): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
	(1, 0, 1, 0, 0, 1, 0): 7,
	(1, 1, 1, 1, 1, 1, 1): 8,
	(1, 1, 1, 1, 0, 1, 1): 9
}

# load the example image
path_to_image = '/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/Images/test_image_friday.png'
image1 = cv2.imread(path_to_image)
cv2.imwrite('/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/Images/Processed_Images/image_read.PNG', image1)
image = Image.open("/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/Images/Processed_Images/image_read.PNG")

# pre-process the image by resizing it, converting it to
# graycale, blurring it, and computing an edge map

image = imutils.resize(image1, height=500)
gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 60, 200, 255)
cv2.imwrite('/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/Images/Processed_Images/image_edge.PNG', edged)

# find contours in the edge map, then sort them by their
# size in descending order
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
displayCnt = None

# loop over the contours
# for c in cnts:
#     # approximate the contour
#     peri = cv2.arcLength(c, True)
#     approx = cv2.approxPolyDP(c, 0.02 * peri, True)
#     # if the contour has four vertices, then we have found
#     # the thermostat display
#     if len(approx) == 4:
#         displayCnt = approx
#         break

###################
#Define path to tessaract.exe
path_to_tesseract = '/usr/local/Cellar/tesseract/5.2.0/bin/tesseract'

#Point tessaract_cmd to tessaract.exe
pytesseract.tesseract_cmd = path_to_tesseract

def screen_reader(path):
    '''
    takes image path as input, outputs values on erg screen
    adjust dilation, erosion and enhancement values for increased accuracy
    make additional function to loop through many images
    '''
    #Image.MAX_IMAGE_PIXELS = None
    img = cv2.imread(path)
    #img = imutils.rotate(img, angle=90)
    img = cv2.resize(img, (0,0), fx=3, fy=3)
    cv2.imwrite("/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/Images/Processed_Images/new.png", img)

    img1 = cv2.imread("/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/Images/Processed_Images/new.png", 0)

    #Apply dilation and erosion
    kernel = np.ones((2, 2), np.uint8)
    img1 = cv2.dilate(img1, kernel, iterations=1)
    img1 = cv2.erode(img1, kernel, iterations=1)

    img1 = cv2.adaptiveThreshold(img1,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,4)

    cv2.imwrite("/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/Images/Processed_Images/new1.png", img1)
    img2 = Image.open("/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/Images/Processed_Images/new1.png")

    #Enhance the image
    img2 = img2.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(img2)
    img2 = enhancer.enhance(10)
    img2.save('/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/Images/Processed_Images/new2.png')

    screen_stats = pytesseract.image_to_string(Image.open("/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/Images/Processed_Images/new2.png"))
    return screen_stats

#Define path to image, no path if in strava webscraping. Get from apple photo library
#path_to_image = '/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/Images/test_image_friday.png'
#print(screen_reader(path_to_image))



