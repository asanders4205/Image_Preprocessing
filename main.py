import os
import kagglehub
from PIL import Image, UnidentifiedImageError
import shutil



def images_are_loaded(path: str) -> int:
    '''Check if the image dataset is loaded already
        See if 

    '''






def verify_files(path: str, target_size: tuple[int,int] = (512, 512)) -> None:
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



    # Check each file in the directory
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
        with Image.open(image_path) as img:     # Open image file and find the size

            # Image is not the proper size
            if img.size != target_size:

                # Give error message
                # print(f"Improperly sized file: {file_name}: {img.size}")

                # Resize the image and save
                print(f'Resizing image {file_name}')

                resized_img = img.resize(target_size)
                updated_filename = f"resized_{resized_counter}{ext}" # A file counter for resized images, and the saved file extension
                resized_img.save(os.path.join(path, updated_filename))

    print(f'Files validated. All images are of size {target_size}')


def main():

    # Grab the part of the URL after kaggle.com/datasets/   and assign it to kaggle_path
    
    
    
    # kaggle_path = "nisarahmedrana/biq2021"
    # data_path = kagglehub.dataset_download(kaggle_path)
    data_path = r"C:\\Users\\alecs\\.cache\\kagglehub\\datasets\\nisarahmedrana\\biq2021\versions\\4"


    # Open an image
    sample_image_path = os.path.join(data_path, "Images (1).jpg")  # TODO generalize and adjust based on folder layout
    img = Image.open(sample_image_path)

    verify_files(data_path)




if __name__=="__main__": 
    main()