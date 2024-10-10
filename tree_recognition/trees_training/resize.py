from PIL import Image
import os
import pathlib
from concurrent.futures import ThreadPoolExecutor

TRAINING_ROOT = "originals"
IMAGE_SIZE = (1080, 1080)
SAVE_DIR = "resized"


def resize(filename: str, dirpath) -> None:
    """Applies all the preprocessing to a given image file
    inside the given directory path."""
    # open the image
    filepath: str = os.path.join(dirpath, filename)
    image: Image.Image = Image.open(filepath)

    # apply filters
    image.thumbnail(IMAGE_SIZE)

    # save the images at the end
    class_name: str = pathlib.PurePath(dirpath).name
    save_path: str = f"{SAVE_DIR}/{class_name}/{filename}"
    if not os.path.exists(pathlib.Path(save_path).parent):
        os.makedirs(pathlib.Path(save_path).parent)
    image.save(save_path)
    image.close()


def main():
    for dirpath, _, filenames in os.walk(TRAINING_ROOT):
        if not filenames:
            continue
        print("resizing:", filenames)
        # multithreading - I am speed
        with ThreadPoolExecutor() as executor:
            executor.map(resize, filenames, [dirpath] * len(filenames))


if __name__ == "__main__":
    main()
