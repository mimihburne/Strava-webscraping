from pytesseract import pytesseract
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import cv2
import pandas as pd
import os
import imutils
from os import listdir

#Define path to tessaract.exe
path_to_tesseract = '/usr/local/Cellar/tesseract/5.2.0/bin/tesseract'

#Point tessaract_cmd to tessaract.exe
pytesseract.tesseract_cmd = path_to_tesseract

def screen_reader(path):
    '''
    takes image path as input, outputs values on erg screen
    adjust dilation, erosion and enhancement values for increased accuracy
    make additional function to loop through many images, or have column plot of many?
    '''
    #read input image, convert to grayscale
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #remove shadows, cf. https://stackoverflow.com/a/44752405/11089932
    dilated_img = cv2.dilate(gray, np.ones((7, 7), np.uint8), iterations=1)
    dilated_img = cv2.erode(dilated_img, np.ones((7, 7), np.uint8), iterations=1)
    bg_img = cv2.GaussianBlur(dilated_img, (7, 7), 0)
    #bg_img = cv2.medianBlur(dilated_img, 21)
    diff_img = 255 - cv2.absdiff(gray, bg_img)

    norm_img = np.zeros((diff_img.shape[0], diff_img.shape[1]))
    norm_img = cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

    #work_img = norm_img -- better with this although pytesseract prefers black bg
    T, work_img = cv2.threshold(norm_img, 200, 255, cv2.THRESH_BINARY_INV)
    #work_img = cv2.adaptiveThreshold(norm_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,2)
    #work_img = cv2.threshold(norm_img, 0, 255, cv2.THRESH_OTSU)[1]

    #Enhance the image
    work_img = Image.fromarray(work_img)
    work_img = work_img.convert("RGB")
    enhancer = ImageEnhance.Contrast(work_img)
    work_img = enhancer.enhance(2.0)

    custom_config = r'--oem 3 --psm 6'
    work_img.save("Additional_Data/Images/Processed_Images/new3.png")
    screen_stats = pytesseract.image_to_string(work_img, config=custom_config)
    return screen_stats

#Define path to image, no path if in strava webscraping. Get from apple photo library
path_to_image = '/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/columnplot.png'
print(screen_reader(path_to_image))



################################
def data_from_screen(folder):
    erg_data = pd.DataFrame(
        columns=[
            "date",
            "title",
            "elapsed_time",
            "moving_time",
            "distance",
            "average_split",
            "average_cadence"
        ]
    )
    # Get the file names in the directory
    for i in os.listdir(folder):
        print(i)
        #print(screen_reader(i))
        '''screen = screen_reader(i)#path to specified picture- loop through directory
        #nlines = len(screen.splitlines())
        lines = screen.split('\n')

        erg_data.loc[i, "date"] = "date"  # date and time: extract from image
        erg_data.loc[i, "title"] = lines[0].removesuffix(' Total Time:')
        erg_data.loc[i, "elapsed_time"] = lines[2].split()[2]
        erg_data.loc[i, "moving_time"] = lines[5].split()[0]
        erg_data.loc[i, "distance"] = lines[5].split()[1]
        erg_data.loc[i, "average_split"] = lines[5].split()[2]
        erg_data.loc[i, "average_cadence"] = lines[5].split()[3]
    return erg_data'''
'''
    interval_time = []
    interval_distance = []
    interval_split = []
    interval_rate = []
    interval_end_heartrate =[]
    for i in range (7, nlines-2):
        interval_time.append(lines[7].split()[0])
        interval_distance.append(lines[i].split()[1])
        interval_split.append(lines[7].split()[2])
        interval_rate.append(lines[7].split()[3])
        interval_end_heartrate.append(lines[7].split()[4])
        #add these to a separate df
        '''
#folder = 'Additional_Data/test images'

#print(data_from_screen(folder))

#automate photo transfer from photos->erg into chosen directory
#find directory for album within photos

'''

#test with 2 screens

#extract date n time
#extract datatypes'''
