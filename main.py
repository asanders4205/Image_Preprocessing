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


def preprocess_images(path: str, target_size: tuple[int, int] = (512, 512)) -> None:
    """
    Runs both verification steps: file type and image size.
    """
    verify_files_are_images(path)
    verify_images_are_uniform_size(path, target_size)
    # print('Pixels normalized')





def normalize_pixel_values(maximum_pixel_value: float = 255.0, path: str):
    '''Constant brightness
    Param: Max pixel value, default of 255.0
    '''

    for file_name in sorted(os.listdir(path)):
        img = cv2.imread(file_name)
        normalized = img / maximum_pixel_value


print(f'Image pixels normalized. All images are of size {target_size}')




def main():
    
    # Load dotenv
    load_dotenv()


    data_path = r'input_images'
    images_origin = os.getenv("images_filepath") # Name of variable in .env file

    #Verify images are loaded
    if images_not_loaded(data_path, images_origin):
        print('Directories are different, verifying input...')
        preprocess_images(data_path)
    else:
        print("Direcories the same, moving on.")

    # normalize pixels via Min Max (dividing by the max value)
    # normalize_pixel_values() #TODO uncomment



if __name__=="__main__": 
    main()
