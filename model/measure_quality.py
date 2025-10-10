import pandas as pd
import os
import cv2 as cv
import numpy as np
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

'''Loop over directory, return variance for each image?'''
def measure_blur(directory_path): # Return a dataframe
    # define threshold
    threshold = 100.0
    
    # Define series
    blurriness_ratings = []
    
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
        if fm < threshold:
            text = "Blurry"
        
        blurriness_ratings.append(fm)
        '''# show the image
        cv.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
            cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        cv.imshow("Image", image)
        key = cv.waitKey(0)'''
    # End for

    return blurriness_ratings



# Call functions (when running, include import statements)
# key = 'full_images_filepath'
# input_path = os.getenv(key)
# measure_blur(input_path)


image_blurs = measure_blur('data/input_images')

print(image_blurs[:5])


'''

    # Convert csv to df
    df = pd.read_csv(directory_path)

    # Get number of ratings
    num_of_ratings = blurriness_ratings.size

    # Make sure there's a rating for every image
    assert df.length == num_of_ratings

    # print(f'df length: {df.length}')

    # print(f'num_of_ratings: {num_of_ratings}')

'''




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
