import os
from dotenv import load_dotenv

def images_loaded(folder_1: str, folder_2: str) -> bool:
    '''Check if the image dataset is loaded already
        See if directory contents are the same quantity
        No parameters
        Return true or false
    '''

    folder_1 = "input_images"
    count_1 = sum(1 for f in os.listdir(folder_1) if os.path.isfile(os.path.join(folder_1, f)))

    # Replace with env variable - make portable for other users
    load_dotenv()

    folder_2 = os.getenv("images_filepath")

    count_2 = sum(1 for f in os.listdir(folder_2) if os.path.isfile(os.path.join(folder_2, f)))

    count_diff = count_1 - count_2
    # print(f'count_diff: {count_diff}')

    if count_diff == 0:
        return True
    else:
        return False