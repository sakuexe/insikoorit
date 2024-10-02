from PIL import Image
import os
import pathlib
import random
from PIL import ImageFilter, ImageEnhance

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
    return image

def rotate_images(image) -> None:
    #random rotation
    a = [0,90,180,270]
    random.shuffle(a)
    ang = a[0]
    image = image.rotate(ang)
    print(ang)
    return image
def filter_images(image) -> None:
    #filter random
    r = random.randint(0,3)
    match r:
        case 0:
            image = image.filter(ImageFilter.BLUR)
        case 1:
            image = image.filter(ImageFilter.SHARPEN)
        case 2:
            image = image.filter(ImageFilter.SMOOTH)
        case 3:
            pass
    print(r)
    return image
def contrast_images(image) -> None:
    #random color
    #contrast
    c = 1.0
    if random.random()*1>0.5:
        c = random.random()*1 + 0.5
        image = ImageEnhance.Contrast(image).enhance(c)
    print(c)
    return image
   
def save_images(image, image_path: str) -> None:
    save_path = f"edited_{image_path}"
    if not os.path.exists(pathlib.Path(save_path).parent):
        os.makedirs(pathlib.Path(save_path).parent)
    print(save_path)
    image.save(save_path)
    image.close()


def preprocess(filepath: str) -> None:
    """Applies all the preprocessing to a given file."""
    image = crop_images(filepath)
    # TODO: add more preprocessing, like random rotation or color 
    print("Cropped")
    image = rotate_images(image)
    image = filter_images(image)
    image = contrast_images(image)
    save_images(image, filepath)
    
for dirpath, dirnames, filenames in os.walk(TRAINING_ROOT):
    if not filenames:
        continue

    for filename in filenames:
        preprocess(os.path.join(dirpath, filename))
