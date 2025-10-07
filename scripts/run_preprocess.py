import os
from dotenv import load_dotenv
from pathlib import Path


from preprocess.transform import preprocess_images

def main():
    
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





# if __name__=="__main__": 
#     main()
