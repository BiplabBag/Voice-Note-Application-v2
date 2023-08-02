# ocr_module.py
import os
import pytesseract
import cv2
import math
from scipy.signal import convolve2d
import numpy as np

# Set the path to the Tesseract executable (change this if necessary)
#base_path = os.path.abspath(os.path.dirname(__file__))
#tesseract_path = os.path.join(base_path, 'tesseract.exe')



#estimating noise in the image where sigma is the measure of noise in image
def estimate_noise(I):

  H, W = I.shape

  M = [[1, -2, 1],
       [-2, 4, -2],
       [1, -2, 1]]

  sigma = np.sum(np.sum(np.absolute(convolve2d(I, M))))
  sigma = sigma * math.sqrt(0.5 * math.pi) / (6 * (W-2) * (H-2))

  return sigma 

#bluring and median filtering
def filter_img(a):
    blur = cv2.GaussianBlur(a,(3,3),0)  #blur
    med_blur = cv2.medianBlur(blur, 3)  #median filter
    return med_blur

def ocr_image(image_path):
    """
    Perform OCR on the given image and return the extracted text.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Extracted text from the image.
    """
    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sigma = estimate_noise(gray)
    
    #if estimated noise is greater then 15 then use filtering and then use Otsu Threshold
    #else use adaptive threshold for smooth image
    if sigma > 15:
        processed_img = filter_img(gray)
        ret,th = cv2.threshold(processed_img, 180,255,cv2.THRESH_BINARY,cv2.THRESH_OTSU)
    else:
        th = cv2.adaptiveThreshold(gray, 230, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 5)

    thresh, im_bw_inv = cv2.threshold(th, 200, 255, cv2.THRESH_BINARY_INV) #inverting image intensity

    #dilating image for increasing thickness if charecter
    kernel = np.ones((2,2),np.uint8) 
    dilated_image = cv2.dilate(im_bw_inv,kernel,iterations = 1) 

    thresh, im_bw = cv2.threshold(im_bw_inv, 200, 255, cv2.THRESH_BINARY_INV) #invering again into original colour   

    print(pytesseract.image_to_string(im_bw)) # extrcting strings 

    text = pytesseract.image_to_string(im_bw)
    return text
