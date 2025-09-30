from PIL import Image, UnidentifiedImageError


import os
import shutil


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