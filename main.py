import os
import kagglehub
from PIL import Image, UnidentifiedImageError
import shutil

''' Selection:  identify and collect relevant data.
    Loading dataset'''
# Load dataset from Kaggle
path = kagglehub.dataset_download("nisarahmedrana/biq2021")
# print("Dataset files stored at:", path)


def verify_files(path: str) -> None:
    '''
        Accepts a filepath
        Verifies that all files in the directory are images
            - If a non-image file is found, move to bad_files folder (created within the function)
            - Sets a uniform image size and resizes all images uniformly if necessary
                - Sets to (512, 512) by default
    '''

    # Open an image
    sample_image_path = os.path.join(path, "Images (1).jpg")  # adjust based on folder layout
    img = Image.open(sample_image_path)


    target_size = (512, 512)
    valid_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}

    # Repository for bad files
    bad_dir = 'bad_files'
    os.makedirs(bad_dir, exist_ok=True)


    # Check each file in the directory
    for file_name in os.listdir(path):

        ''' Grab the file extension    # _ is a throwaway variable  ext will hold the file extension
        '''
        _, ext = os.path.splitext(file_name)

        # Ensure lowercase
        ext = ext.lower()

        # Store location of image
        image_path = os.path.join(path,file_name)

        # Verify all files are images (have file extensions in the list of known image formats)
        if ext not in valid_exts:
            print(f'Non-image file found: {file_name}')
            # image_path = os.path.join(path,file_name)

            # Move non-image files to other folder
            try:
                with Image.open(image_path) as img:
                    img.verify()

            except UnidentifiedImageError:
                print(f'Moving {file_name} to bad_files/')
                shutil.move(image_path, bad_dir)

        # Open and find the image size
        with Image.open(image_path) as img:

            # Image is not the proper size (512, 512)
            if img.size != target_size:
                # print(f"Improperly sized file: {file_name}: {img.size}")
                print(f'Resizing image {file_name}')
                image_path = img.resize((512,512))
                # img = img.resize((512,512)) # This does not resize the image, only the loop variable