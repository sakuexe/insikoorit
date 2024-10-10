from PIL import Image
from PIL import ImageFilter, ImageEnhance
import os
import pathlib
import random
from concurrent.futures import ThreadPoolExecutor

TRAINING_ROOT = "originals"
IMAGE_SIZE = (1080, 1080)
SAVE_DIR = "edited"


def crop_image(image: Image.Image) -> Image.Image:
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
    return image


def rotate_image(image: Image.Image) -> Image.Image:
    """Applies a random rotation to the image.
    The possible rotations are in 90 degree intervals."""
    rotate_by_angle = [0, 90, 180, 270]
    image = image.rotate(random.choice(rotate_by_angle))
    return image


def filter_image(image: Image.Image) -> Image.Image:
    """Applies a random image filter to the passed image.
    This filter is either blur, sharpen or smooth."""
    filters = (ImageFilter.BLUR, ImageFilter.SHARPEN, ImageFilter.SMOOTH, None)
    random_filter = random.choice(filters)
    if random_filter is not None:
        image = image.filter(random_filter)
    return image


def contrast_image(image: Image.Image, multiplier=1.5, min_contrast=0.5) -> Image.Image:
    """Applies a random amount of image contrast to the passed image.
    With the multiplier you can change the max strength of the saturation.
    The min_contrast parameter sets the minimum possible contrast factor
    The base value can be between 0.5 and 1.5."""
    factor = random.random() * multiplier + min_contrast
    image = ImageEnhance.Contrast(image).enhance(factor)
    return image


def saturate_image(image: Image.Image, multiplier=1.75, min_saturation=0.25) -> Image.Image:
    """Applies random amount of saturation to the passed image.
    With the multiplier you can change the max strength of the saturation.
    The min_saturation parameter sets the base minimum saturation factor
    The base value is between 0 and 1"""
    factor = random.random() * multiplier + min_saturation
    image = ImageEnhance.Color(image).enhance(factor)
    return image


def preprocess(filename: str, dirpath) -> None:
    """Applies all the preprocessing to a given image file
    inside the given directory path."""
    # open the image
    filepath: str = os.path.join(dirpath, filename)
    image: Image.Image = Image.open(filepath)

    # apply filters
    image = crop_image(image)
    image = rotate_image(image)
    image = filter_image(image)
    image = contrast_image(image)
    image = saturate_image(image)

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
            executor.map(preprocess, filenames, [dirpath] * len(filenames))


if __name__ == "__main__":
    main()
