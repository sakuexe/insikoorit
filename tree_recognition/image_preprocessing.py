from PIL import Image
import os
import pathlib

TRAINING_ROOT = "trees_training"
IMAGE_SIZE = (1080, 1080)


def crop_images(image_path: str) -> None:
    image = Image.open(image_path)
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

    save_path = f"edited_{image_path}"
    if not os.path.exists(pathlib.Path(save_path).parent):
        os.makedirs(pathlib.Path(save_path).parent)

    image.save(save_path)

    image.close()


def preprocess(filepath: str) -> None:
    """Applies all the preprocessing to a given file."""
    crop_images(filepath)
    # TODO: add more preprocessing, like random rotation or color adjustments


for dirpath, dirnames, filenames in os.walk(TRAINING_ROOT):
    if not filenames:
        continue

    for filename in filenames:
        preprocess(os.path.join(dirpath, filename))
