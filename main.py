import os
import kagglehub
from PIL import Image, UnidentifiedImageError
import shutil
import cv2 # Normalising pixels
from dotenv import load_dotenv



def images_not_loaded(folder_1: str, folder_2: str) -> bool:
    '''Check if the image dataset is loaded already
        See if directory contents are the same quantity
        No parameters
        Return true or false
    '''

    folder_1 = "input_images"
    count_1 = sum(1 for f in os.listdir(folder_1) if os.path.isfile(os.path.join(folder_1, f)))

    folder_2 = r"C:\\Users\\alecs\\.cache\\kagglehub\\datasets\\nisarahmedrana\\biq2021\versions\\4"
    count_2 = sum(1 for f in os.listdir(folder_2) if os.path.isfile(os.path.join(folder_2, f)))

    count_diff = count_1 - count_2
    print(f'count_diff: {count_diff}')

    if count_diff == 0:
        return False
    else:
        return True


def preprocess_images(path: str, target_size: tuple[int,int] = (512, 512)) -> None:
    ''' verify_files
        Verifies that all files in a provided directory are uniformly sized images
        If a non-image file is found, move it to bad_files folder (created within the function)
        Parameters:
            path: Filepath to folder containing images
            param_size: Image size: Default is set to (512, 512)
        Return: None
    '''


    valid_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}


    # Repository for bad files
    bad_dir = 'bad_files'
    os.makedirs(bad_dir, exist_ok=True)
    resized_counter = 0 # Count and name resized image
    PIXEL_COUNT = 255.0 # Regular RGB pixel count


    for file_name in sorted(os.listdir(path)):

        prefix = 'resized_image_'
        _, ext = os.path.splitext(file_name)   # Grab the file extension:   _ is a throwaway variable ext will hold the file extension

        # Ensure lowercase
        ext = ext.lower()

        # Store location of image
        image_path = os.path.join(path,file_name)

        # Verify all files are images (have file extensions in the list of known image formats)
        if ext not in valid_exts:
            print(f'Non-image file found: {file_name}')

            # Move non-image files to other folder
            try:
                with Image.open(image_path) as img:
                    img.verify()

            except UnidentifiedImageError:
                print(f'Moving {file_name} to bad_files/')
                shutil.move(image_path, bad_dir)


        # Verify all images are of the same size
        with Image.open(image_path) as img:

            # Image is not the proper size
            if img.size != target_size:

                # Resize the image and save
                print(f'Resizing image {file_name}')

                resized_img = img.resize(target_size)
                updated_filename = f"resized_{resized_counter}{ext}" # A file counter for resized images, and the saved file extension
                resized_img.save(os.path.join(path, updated_filename))

        # Normalise the pixel values - scale to 0 (black) and 1 (white)
        Img = cv2.imread(file_name)
        normalized = img / PIXEL_COUNT

    print(f'Files validated. All images are of size {target_size}')
    print('Pixels normalised')




def main():

    ''' Setting up input
    # Grab the part of the URL after kaggle.com/datasets/   and assign it to kaggle_path
    # kaggle_path = "nisarahmedrana/biq2021"
    # data_path = kagglehub.dataset_download(kaggle_path)
    # data_path = r"C:\\Users\\alecs\\.cache\\kagglehub\\datasets\\nisarahmedrana\\biq2021\versions\\4"

    # sample_image_path = os.path.join(data_path, "Images (1).jpg")  # TODO generalize and adjust based on folder layout
    # img = Image.open(sample_image_path)
    '''
    
    # Load dotenv
    load_dotenv()


    data_path = r'input_images'
    #images_origin = r"C:\\Users\\alecs\\.cache\\kagglehub\\datasets\\nisarahmedrana\\biq2021\versions\\4"
    images_origin = os.getenv("images_filepath") # Name of variable in .env file

    #Verify images are loaded
    if images_not_loaded(data_path, images_origin):
        print('Directories are different, verifying input...')
        preprocess_images(data_path)
    else:
        print("Direcories the same, moving on.")


    # images are of same size and pixels are normalised




if __name__=="__main__": 
    main()