import cv2 #the opencv library. Confusingly, on my system, this is installed as opencv3
import matplotlib.pyplot as plt #for displaying images
import imutils #convienient utils for resizing images
import numpy as np     #an image is just an array of pixels

files = ['/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/test images/IMG_6274.png',
         '/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/test images/IMG_6295.png',
         '/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/test images/IMG_6331.png',
         '/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/test images/IMG_6348.png',
         '/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/test images/IMG_6357.png',
         '/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/test images/IMG_6363.png',
         '/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/test images/IMG_6385.png',
         '/Users/DHB/Documents/My stuff/Strava webscraping/Additional_Data/test images/IMG_6394.png']
names = ["0","1","2","3","4","5","6","7"]

def sideBySidePlot(images):
    n = len(images)
    for i in range(0,n):
        x = plt.subplot(2,4,i+1)
        plt.imshow(images[i], cmap="Greys") #cmap="Greys" doesn't mean grayscale!
        plt.axis('off')
        x.set_title(names[i])
    plt.show()
    plt.savefig('8_test_ims')

def columnPlot(images):
    n = len(images)
    plt.subplots(n,1,figsize=(15,15))
    for i in range(0,n):
        x = plt.subplot(n,1,i+1)
        plt.imshow(images[i], cmap="Greys")
        plt.axis('off')

def resizeTo600(img):
    return imutils.resize(img, height=600)

def toGrayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def bilateralFilter(img):
    return cv2.bilateralFilter(img, 9, 50, 50)

# otsu is a different way of thresholding
# slightly more complicated in that it thresholds based on 'local' brightness
# rather than 'global' thresholds for the whole image
# I'm using it here as another way to try and avoid problems with glare
def otsuThresh(img):
  value,thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
  return thresh

def findBigContours(i,n):
  contours, hierarchy = cv2.findContours(i.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE )
  cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:n]
  cnts = [c for c in cnts if cv2.contourArea(c) > 0]
  return(cnts)

def findContourSquareness(cnt):
  c_area = cv2.contourArea(cnt)
  rect = cv2.minAreaRect(cnt)
  r_area = cv2.contourArea( np.int0(cv2.boxPoints(rect)) )
  return c_area/r_area

def aspectRatio(cnt):
    if cnt is not None:
      m = cv2.minAreaRect(cnt)
      return m[1][0]/m[1][1]
    else:
      return None

def findScreenCnt(cnts):
    screenCnt = None
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        try:
          aspect = aspectRatio(approx)
        except ZeroDivisionError:
          aspect = 10
        if len(approx)==4 and cv2.isContourConvex(approx) and findContourSquareness(approx)>0.9 and aspect > 0.8 and aspect < 1.2:
            screenCnt = approx
            break
    return screenCnt

def extractScreenTransform(original, cnt):
    if cnt is None:
        return None
    ratio = original.shape[0] / 600.0
    pts = cnt.reshape(4, 2)
    rect = np.zeros((4, 2), dtype = "float32")
    # the top-left point has the smallest sum whereas the
    # bottom-right has the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # compute the difference between the points -- the top-right
    # will have the minumum difference and the bottom-left will
    # have the maximum difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # multiply the rectangle by the original ratio
    rect *= ratio
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

    # ...and now for the height of our new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

    # take the maximum of the width and height values to reach
    # our final dimensions
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))

    # construct our destination points which will be used to
    # map the screen to a top-down, "birds eye" view
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

    # calculate the perspective transform matrix and warp
    # the perspective to grab the screen
    M = cv2.getPerspectiveTransform(rect, dst)
    warp = cv2.warpPerspective(original, M, (maxWidth, maxHeight))
    return warp

# Finally put it all together
def extractScreen(img):
    original = img.copy()
    img = resizeTo600(img)
    gray = toGrayscale(img)
    bilat = bilateralFilter(gray)
    otsu = otsuThresh(bilat)
    cnts = findBigContours(otsu, 10)
    screenCnt = findScreenCnt(cnts)
    if screenCnt is not None:
        print( "Found screen (prob. backlit)")
        screen = extractScreenTransform(original, screenCnt)
        return screen
    else:
        cie = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        red = cie[:,:,2]
        otsu = otsuThresh(red)
        cnts = findBigContours(otsu,10)
        screenCnt = findScreenCnt(cnts)
        if screenCnt is not None:
            print("Found screen (prob. not backlit)")
            screen = extractScreenTransform(original, screenCnt)
            return screen

def adaptiveThresh(img):
  return cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)

def extractTotalRow(img):
    original = img.copy()
    img = resizeTo600(img)
    gray = toGrayscale(img)
    bilat = bilateralFilter(gray)
    adap = adaptiveThresh(bilat)
    cnts = findBigContours(adap, 20)
    filteredcnts = [c for c in cnts if (aspectRatio(c) < 0.1 or aspectRatio(c) > 10) and findContourSquareness(c) > 0.9]
    if len(filteredcnts) > 0:
        # if there are contours, pick the biggest one
        totalscnt = filteredcnts[0]
        box = cv2.boxPoints(cv2.minAreaRect(totalscnt))
        totals = extractScreenTransform(original,box)
        return totals
    else:
        # if there aren't apply a CLAHE filter to the image and try again
        clahe = cv2.createCLAHE()
        cl1 = clahe.apply(gray)
        otsu = otsuThresh(cl1)
        cnts = findBigContours(otsu, 20)
        filteredcnts = [c for c in cnts if aspectRatio(c) < 0.1]
        if len(filteredcnts) > 0:
          totalscnt = filteredcnts[0]
          box = cv2.boxPoints(cv2.minAreaRect(totalscnt))
          totals = extractScreenTransform(original,box)
          return totals
        else:
            print("Unable to find totals row")
            return None

originals = [cv2.imread(f) for f in files]

screens = [extractScreen(i) for i in originals]

totals = [extractTotalRow(i) for i in screens]

totals = [i for i in totals if i is not None]

cv2.imwrite(totals_file, totals)
        vision_client = vision.Client()
        with open(totals_file, 'rb') as image_file:
             image = vision_client.image(content=image_file.read())
        texts = image.detect_text()
        return texts

columnPlot(totals)
plt.savefig('columnplot')
'''
from google.cloud import storage
from google.cloud import vision
from google.cloud.vision.feature import Feature
from google.cloud.vision.feature import FeatureTypes
import os
import tempfile

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "YOUR_CREDENTIALS.json"

def cloudAnalysis(filename):
    with tempfile.TemporaryDirectory() as tmpdirname:
        image = cv2.imread(filename)
        screen = extractScreen(image)
        totals = extractTotalRow(screen)
        totals_file = os.path.join(tmpdirname,filename + ".totals.jpg")
        cv2.imwrite(totals_file, totals)
        vision_client = vision.Client()
        with open(totals_file, 'rb') as image_file:
             image = vision_client.image(content=image_file.read())
        texts = image.detect_text()
        return texts

res = [cloudAnalysis(os.path.basename(f)) for f in files]

#https://www.eanalytica.com/Screen-reading-with-open-OpenCV-and-Google/
#save these
#read using first code
#into 1st code df
'''