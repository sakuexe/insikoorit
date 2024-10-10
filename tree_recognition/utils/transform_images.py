import torchvision.transforms as transforms


def get_training_transforms(image_size=256) -> transforms.Compose:
    """Generates a transforms list with a specified image size.
    This transform can then be passed to `torchvision.datasets.ImageFolder`,
    so that these values can be randomized each time the images are trained,
    instead of always using the same preprocessing methods"""
    return transforms.Compose([
        # Random rotation between -30 to 30 degrees
        transforms.RandomRotation(degrees=30),
        # 50% chance of horizontal flip
        transforms.RandomHorizontalFlip(p=0.5),
        # Random crop and resize to 512x512
        transforms.RandomResizedCrop(size=image_size, scale=(0.8, 1.0)),
        # Color jittering
        transforms.ColorJitter(
            brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        # 50% chance of vertical flip
        transforms.RandomVerticalFlip(p=0.5),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[
                             0.229, 0.224, 0.225])
    ])


# apply only a few transforms to validation data
def get_validation_transforms(image_size=256) -> transforms.Compose:
    """Returns a list of transforms values with a specified image size.
    This transform can then be passed to `torchvision.datasets.ImageFolder`,
    so that these values can be randomized each time the images are trained,
    instead of always using the same preprocessing methods"""
    return transforms.Compose([
        # resize to match the training data
        transforms.Resize(image_size),
        # crop to the center of the image
        transforms.CenterCrop(image_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[
                             0.229, 0.224, 0.225])
    ])
