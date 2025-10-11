import pandas as pd
from imutils import paths
import cv2 as cv

# Image quality metrics references:
# - https://www.mathworks.com/help/images/image-quality-metrics.html
# - https://learnopencv.com/image-quality-assessment-brisque/
# - https://pyimagesearch.com/2015/09/07/blur-detection-with-opencv/

def variance_of_laplacian(image):
    """
    Compute the variance of the Laplacian (focus measure) for a grayscale image.
    Higher values indicate a sharper (less blurry) image.
    """
    return cv.Laplacian(image, cv.CV_64F).var()

def measure_blur(directory_path, threshold=100.0):
    """
    Compute a blurriness score (variance of Laplacian) for each image
    found under directory_path.

    Returns:
        list[float]: Blurriness (focus) measures for each image.
    """
    blurriness_ratings = []

    for image_path in paths.list_images(directory_path):
        image = cv.imread(image_path)
        if image is None:
            continue  # Skip unreadable files

        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)

        # Optional classification
        text = "Not Blurry" if fm >= threshold else "Blurry"

        blurriness_ratings.append(fm)

    return blurriness_ratings


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
