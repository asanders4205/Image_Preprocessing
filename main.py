import os
import kagglehub
from PIL import Image, UnidentifiedImageError
import shutil




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


    # Check each file in the directory
    for file_name in os.listdir(path):
        resized_counter = 0 # Count and name resized images
        prefix = 'resized_image_'

        # Grab the file extension:   _ is a throwaway variable ext will hold the file extension
        _, ext = os.path.splitext(file_name)

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
                image_path = img.resize((512,512))

                updated_filename = f"{resized_counter}.{ext}" # A file counter for resized images, and the saved file extension

                image_path.save(os.path.join(updated_filename))

    print(f'Files validated. All images are of size {target_size}')


def main():

    data_path = kagglehub.dataset_download("nisarahmedrana/biq2021")

    # Open an image
    sample_image_path = os.path.join(data_path, "Images (1).jpg")  # TODO generalize and adjust based on folder layout
    img = Image.open(sample_image_path)

    #image_size = (512, 512)

    verify_files(data_path)

    #TODO rename all images so there is not a space in the name
    #TODO resize_image function


    #TODO Find out why the contents of /data are not remaining in the folder between runs



if __name__=="__main__": 
    main()