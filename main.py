import os
import kagglehub
from PIL import Image, UnidentifiedImageError
import shutil
import cv2
from dotenv import load_dotenv
import time
import numpy as np




def images_loaded(folder_1: str, folder_2: str) -> bool:
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
    # print(f'count_diff: {count_diff}')

    if count_diff == 0:
        return True
    else:
        return False

def images_normalized(input_path: str, normalized_images_path: str) -> bool:
    '''Count num images in input and normalized folders'''
    num_input = len(os.listdir(input_path)) #num of images in input folder
    num_normalized = len(os.listdir(normalized_images_path))

    if (num_input != num_normalized):
        print(f'{input_path} and {normalized_images_path} have differing numbers of files')
        return False
    else:
        return True


def verify_files_are_images(path: str) -> None:
    """
    Verifies that all files in a provided directory are images.
    If a non-image file is found, move it to bad_files folder.
    """
    valid_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}
    bad_dir = 'bad_files'
    os.makedirs(bad_dir, exist_ok=True)

    for file_name in sorted(os.listdir(path)):
        _, ext = os.path.splitext(file_name)
        ext = ext.lower()
        image_path = os.path.join(path, file_name)

        if ext not in valid_exts:
            print(f'Non-image file found: {file_name}')
            try:
                with Image.open(image_path) as img:
                    img.verify()
            except UnidentifiedImageError:
                print(f'Moving {file_name} to bad_files/')
                shutil.move(image_path, bad_dir)


def verify_images_are_uniform_size(path: str, target_size: tuple[int, int] = (512, 512)) -> None:
    """
    Verifies that all images in the directory are of the same size.
    Resizes images that are not the correct size.
    """
    valid_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}
    resized_counter = 0

    for file_name in sorted(os.listdir(path)):
        _, ext = os.path.splitext(file_name)
        ext = ext.lower()
        if ext not in valid_exts:
            continue

        image_path = os.path.join(path, file_name)
        with Image.open(image_path) as img:
            if img.size != target_size:
                print(f'Resizing image {file_name}')
                resized_img = img.resize(target_size)
                updated_filename = f"resized_{resized_counter}{ext}"
                resized_img.save(os.path.join(path, updated_filename))
                resized_counter += 1

    print(f'Files validated. All images are of size {target_size}')


def process_filenames(path: str):
    '''Remove certain characters from filenames
    '''
    print('Processing filenames')
    replacements = {" ":"_", "(":"", ")":""}
    files = sorted(os.listdir(path))
    counter = 0

    for file_name in files:
        new_name = file_name
        # counter += 1
        for old,new in replacements.items():
            new_name = new_name.replace(old, new)
            
        if new_name != file_name: # Rename if changed
            old_path = os.path.join(path, file_name)
            new_path = os.path.join(path, new_name)
            os.rename(old_path, new_path)
            counter += 1

    print(f'Filenames processed: {counter} filenames changed')



def preprocess_images(path: str, target_size: tuple[int, int] = (512, 512)) -> None:
    """
    Runs verification steps: file type, image size, process filenames and normalize pixel values
        #TODO consider mulithreading
        #TODO consider adding boolean check functions for each processing function
    """

    verify_files_are_images(path)
    verify_images_are_uniform_size(path, target_size)
    process_filenames(path)


    if not images_normalized(path, 'normalized'):
        normalize_pixel_values(path)


def sharpen_images(path: str): #FIXME - Saves images in parent folder
    #Sharpen images with cv2.filter2D()

    start = time.perf_counter() # Start clock

    # Create the sharpening kernel
    kernel = np.array([
        [0,-1,0],
        [-1,5,-1],
        [0,-1,0]
    ]) # end kernel


    for file_name in sorted(os.listdir(path)):
        file_path = os.path.join(path,file_name)
        img = cv2.imread(file_path)
        if img is None:
            print(f'Could not read {file_name}')
            continue

        # Sharpen the image
        save_img = cv2.filter2D(img, -1, kernel)

        out_path = os.path.join(path, file_name)
        cv2.imwrite(out_path, save_img)

    elapsed = time.perf_counter() - start # End clock
    print(f'Sharpened images - Elapsed time: {round(elapsed,2)} seconds')



def normalize_pixel_values(path: str, maximum_pixel_value: float = 255.0):
    '''Constant brightness
    Param: Max pixel value, default of 255.0
    '''



    start = time.perf_counter() # Start clock

    if not os.path.exists('normalized'):
        os.makedirs('normalized')



    output_dir = os.path.join(path, 'normalized') # Make directory of normalized images
    os.makedirs(output_dir, exist_ok=True)

    for file_name in sorted(os.listdir(path)):
        file_path = os.path.join(path,file_name)
        img = cv2.imread(file_path)
        if img is None:
            print("Could not read {file_path}")
            continue
        normalized = img/ maximum_pixel_value

        # Scale for saving
        save_img = (normalized * 255).astype('uint8')

        out_path = os.path.join(output_dir, file_name)
        cv2.imwrite(out_path, save_img)

    elapsed = time.perf_counter() - start # End clock
    print(f'Image pixels normalized to {maximum_pixel_value}')
    print(f'Elapsed time - Normalizing pixel values: {round(elapsed,2)} seconds')



def import_dataset_from_kaggle(url: str) -> str:
    '''
        Get images from kaggle dataset 
        Input: URL
        Output: Local filepath in .cache/kagglehub
    '''
    # Download latest version
    output_path = kagglehub.dataset_download(url)

    print('Downloaded dataset from {url}\n to folder: {output_path}')

    return output_path


def main():
    


    # Load dotenv
    load_dotenv()


    # URL
    # kaggle_url = 'https://www.kaggle.com//datasets//nisarahmedrana//biq2021'



    # Import kaggle images
    # images_origin = kagglehub.dataset_download("nisarahmedrana/biq2021") # TODO make a trigger for downloading the files from kaggle
    # print("Path to dataset files:", images_origin)
    images_origin = os.getenv('images_filepath')

    data_path = r'input_images' # Hold images in project directory for development
    # images_origin = import_dataset_from_kaggle(kaggle_url)


    #Verify images are loaded
    
    # if not images_loaded(data_path, images_origin): # TODO Can eliminate and run project from .cache/kagglehub
    #     print('Loading and processing images...')
    preprocess_images(data_path) # verify images, verify size, process filenames, normalize pixel values
    # else:
    #     print("Directories the same, moving on.")
    

    # print('normalizing pixel values (main)')
    normalize_pixel_values(data_path)

    # Sharpen images
    # sharpen_images(data_path) #FIXME






if __name__=="__main__": 
    main()
