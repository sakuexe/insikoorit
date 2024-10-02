from PIL import Image
import os
import pathlib
import concurrent.futures

TRAINING_ROOT = "trees_training"
IMAGE_SIZE = (1080, 1080)


def crop_images(image: Image.Image):
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

    image = image.crop((left, top, right, bottom))

    image.thumbnail(IMAGE_SIZE)


def preprocess(filename: str, dirpath: str) -> None:
    """Applies all the preprocessing to a given file."""
    filepath = os.path.join(dirpath, filename)
    image = Image.open(filepath)
    # TODO: add more preprocessing, like random rotation or color adjustments.
    # always pass the image-variable, so that all the effects get
    # applied to the same instance, that will be saved afterwards.
    crop_images(image)

    # close and save the image when all processing is done
    save_path = f"edited_{filepath}"
    if not os.path.exists(pathlib.Path(save_path).parent):
        os.makedirs(pathlib.Path(save_path).parent)

    image.save(save_path)
    image.close()


for dirpath, dirnames, filenames in os.walk(TRAINING_ROOT):
    if not filenames:
        continue

    # execute the preprocessing in parallel using multithreading
    # for speediness
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(preprocess, filenames, [dirpath] * len(filenames))
