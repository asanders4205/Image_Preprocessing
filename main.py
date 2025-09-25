import os
import kagglehub
from PIL import Image, UnidentifiedImageError
import shutil
import cv2
from dotenv import load_dotenv
import time
import numpy as np
from pathlib import Path



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


def verify_files_are_images(path: str) -> None:
    """
    Verifies that all files in a provided directory are images.
    If a non-image file is found, move it to bad_files folder.
    """
    print(f'Arg to verify fils are images: {path}')
    valid_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}
    bad_dir = 'bad_files'
    os.makedirs(bad_dir, exist_ok=True)


    for file_name in (os.listdir(path)):

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


def preprocess_images(input_images_folder: str, target_size: tuple[int, int] = (512, 512)) -> None:
    """
    Runs verification steps: file type, image size, process filenames and normalize pixel values
        # consider mulithreading
        # consider adding boolean check functions for each processing function
    """


    print(f'Calling verify_files_are_images with argument {input_images_folder}')
    verify_files_are_images(input_images_folder)

    print(f'Calling verify_images_are_uniform_size with argument {input_images_folder}')
    verify_images_are_uniform_size(input_images_folder, target_size)



    print(f'Calling process_filenames with argument {input_images_folder}')    
    process_filenames(input_images_folder)


    current_dir = os.getcwd()

    normalize_pixel_values(current_dir)


def sharpen_images(path: str):
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
            print(f'Could not read {file_name} (msg source: sharpen_images)')
            continue

        # Sharpen the image
        save_img = cv2.filter2D(img, -1, kernel)

        # Save in the original file, overwriting the unsharpened image
        out_path = os.path.join(path, file_name)
        cv2.imwrite(out_path, save_img)

    elapsed = time.perf_counter() - start # End clock
    print(f'Sharpened images - Elapsed time: {round(elapsed,2)} seconds')


def normalize_pixel_values(working_directory: str, maximum_pixel_value: float = 255.0) -> str:
    ''' Works from current working directory to access /normalized and /input_images

    Constant brightness

    Param:
        working_directory: Working directory, contains this program /input_images and /normalized
        Max pixel value, default of 255.0

        Returns String: Filepath of normalized image directory
    '''
    print(f'Normalizing pixel values to {maximum_pixel_value} ...')

    # Start timer
    start = time.perf_counter() # Start clock
    last_print = start
    print_interval = 10 # seconds

    # Progress tracker
    path = os.path.join(working_directory, 'normalized')
    images_qty_denom = sum(1 for entry in os.listdir(path) if os.path.isfile(os.path.join(path, entry)))


    images_qty_num = 0 # Image counter variable: used as numerator
    
    if not os.path.exists('normalized'):
        os.makedirs('normalized')



    normalized_images_directory = os.path.join(working_directory, 'normalized') # Directory for normalized images
    os.makedirs(normalized_images_directory, exist_ok=True)

    input_images_directory = os.path.join(working_directory, 'input_images')
    for file_name in sorted(os.listdir(input_images_directory)):
        file_path = os.path.join(input_images_directory, file_name)
        img = cv2.imread(file_path)
        if img is None:
            print(f'Could not read {file_path} (msg source: normalize_pixel_values)')
            continue
        normalized = img/ maximum_pixel_value

        # Scale for saving
        save_img = (normalized * 255).astype('uint8')

        # Iterate counter
        images_qty_num += 1

        out_path = os.path.join(normalized_images_directory, file_name)
        cv2.imwrite(out_path, save_img)

        # Inside loop: Print elapsed time every 10 seconds
        now = time.perf_counter()
        if now - last_print >= print_interval:
            elapsed = now - start
            print(f'Elapsed: {elapsed:.2f} seconds')
            last_print = now

            print(f'Images processed: {images_qty_num}/{images_qty_denom}')



    elapsed = time.perf_counter() - start # End clock
    print(f'Image pixels normalized to {maximum_pixel_value}')
    print(f'Elapsed time - Normalizing pixel values: {round(elapsed,2)} seconds')

    return normalized_images_directory


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

    images_origin = os.getenv('images_filepath')

    working_directory= os.getcwd()
    print(f'working_directory: {working_directory}')

    input_images_folder = os.path.join(working_directory, 'input_images')

    print('Loading and processing images...')
    preprocess_images(input_images_folder) # verify images, verify size, process filenames, normalize pixel values
    

    # print('normalizing pixel values (main)')
    # normalize_pixel_values(working_directory,)

    # Sharpen images
    # sharpen_images(#normalized directory here)





if __name__=="__main__": 
    main()
