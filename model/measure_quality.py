import pandas as pd
import os
import cv2 as cv
import numpy as np
# from imutils import paths #A series of convenience functions to make basic image processing functions such as translation, rotation, resizing, skeletonization, displaying Matplotlib images, sorting contours, detecting edges, and much more easier with OpenCV and both Python 2.7 and Python 3
import argparse
from imutils import paths

# Image qualtiy metrics
# https://www.mathworks.com/help/images/image-quality-metrics.html
# https://learnopencv.com/image-quality-assessment-brisque/
# blur with opencv https://pyimagesearch.com/2015/09/07/blur-detection-with-opencv/

def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv.Laplacian(image, cv.CV_64F).var()


def measure_blur(directory_path):
    # loop over the input images
    for imagePath in paths.list_images(directory_path):
        # load the image, convert it to grayscale, and compute the
        # focus measure of the image using the Variance of Laplacian
        # method
        image = cv.imread(imagePath)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)
        text = "Not Blurry"
        # if the focus measure is less than the supplied threshold,
        # then the image should be considered "blurry"
        if fm < args["threshold"]:
            text = "Blurry"
        # show the image
        cv.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
            cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        cv.imshow("Image", image)
        key = cv.waitKey(0)








        



# Call functions (when running, include import statements)
measure_blur('data\input_images')









    # src = 'data/input_images/Images_1.jpg' # sample image
    
    # # Read image
    # image = cv.imread(src)
    # if image is None:
    #       raise FileNotFoundError(f'Could not read image at {src}')
    

    #  # Convert the image to grayscale
    # # src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    
    # src_gray = cv.imread(src,cv.IMREAD_GRAYSCALE)
    
    # cv.imshow("Image", src_gray)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
