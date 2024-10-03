from PIL import Image
from PIL import ImageFilter, ImageEnhance
import os
import pathlib
import random
from concurrent.futures import ThreadPoolExecutor

TRAINING_ROOT = "trees_training/originals"
IMAGE_SIZE = (1080, 1080)
SAVE_DIR = "trees_training/edited"


def crop_images(image: Image.Image) -> None:
    """Crops and resizes the passed image.
    The cropping will be done to a square aspect ratio."""
    width, height = image.size
    left, right, top, bottom = [0] * 4

    if width > height:
        left = (width - height) / 2
        right = (width + height) / 2
        top = 0
        bottom = height

    if width < height:
        left = 0
        right = width
        top = (height - width) / 2
        bottom = (height + width) / 2

    # crop the image
    image = image.crop((left, top, right, bottom))
    # resize the image
    image.thumbnail(IMAGE_SIZE)


def rotate_images(image: Image.Image) -> None:
    """Applies a random rotation to the image.
    The possible rotations are in 90 degree intervals."""
    rotate_by_angle = [0, 90, 180, 270]
    image = image.rotate(random.choice(rotate_by_angle))


def filter_images(image: Image.Image) -> None:
    """Applies a random image filter to the passed image.
    This filter is either blur, sharpen or smooth."""
    filters = (ImageFilter.BLUR, ImageFilter.SHARPEN, ImageFilter.SMOOTH)
    image = image.filter(random.choice(filters))


def contrast_images(image: Image.Image) -> None:
    """Applies a random amount of image contrast to the passed image.
    This value can be between 0.5 and 1.5."""
    contrast = random.random() + 0.5
    image = ImageEnhance.Contrast(image).enhance(contrast)


def preprocess(filename: str, dirpath) -> None:
    """Applies all the preprocessing to a given image file
    inside the given directory path."""
    filepath: str = os.path.join(dirpath, filename)
    image: Image.Image = Image.open(filepath)

    # apply filters -
    # the image variable can just be passed as a reference here
    crop_images(image)
    rotate_images(image)
    filter_images(image)
    contrast_images(image)

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
        # multithreading - I am speed
        with ThreadPoolExecutor() as executor:
            executor.map(preprocess, filenames, [dirpath] * len(dirpath))


if __name__ == "__main__":
    main()
