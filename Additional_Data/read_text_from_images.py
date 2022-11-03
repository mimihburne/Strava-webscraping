from PIL import Image, ImageEnhance
import cv2
from pytesseract import pytesseract
#import os

#Define path to tessaract.exe
path_to_tesseract = '/usr/local/Cellar/tesseract/5.2.0/bin/tesseract'

#Define path to image, no path if in strava webscraping. Get from apple photo library
path_to_image = 'Images/IMG_6394 Small.png'

#Point tessaract_cmd to tessaract.exe
pytesseract.tesseract_cmd = path_to_tesseract

#Open image with PIL
img = Image.open(path_to_image)
#enhancer = ImageEnhance.Contrast(img)
#factor = 1.5 #increase contrast
#im_output = enhancer.enhance(factor)
#im_output.save('more-contrast-image.png')
#img1 = Image.open('more-contrast-image.png')
#Extract text from image
#text = pytesseract.image_to_string(img1)
#print(text[:-1])


img2 = cv2.imread(path_to_image)
gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
cv2.imwrite('threshold_image.jpg',thresh1)
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 12))
dilation = cv2.dilate(thresh1, rect_kernel, iterations = 3)
cv2.imwrite('dilation_image.jpg',dilation)
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
im2 = img2.copy()
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)

    # Draw the bounding box on the text area
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Crop the bounding box area
    cropped = im2[y:y + h, x:x + w]

    cv2.imwrite('rectanglebox.jpg', rect)

    # open the text file
    file = open("text_output2.txt", "a")

    # Using tesseract on the cropped image area to get text
    text = pytesseract.image_to_string(cropped)

    # Adding the text to the file
    file.write(text)
    file.write("\n")

    # Closing the file
    file.close

'''
For multiple images
#Get the file names in the directory
for root, dirs, file_names in os.walk(path_to_images):
    #Iterate over each file name in the folder
    for file_name in file_names:
        #Open image with PIL
        img = Image.open(path_to_images + file_name)

        #Extract text from image
        text = pytesseract.image_to_string(img)

        print(text)
'''