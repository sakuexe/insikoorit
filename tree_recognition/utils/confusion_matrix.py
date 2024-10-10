import torch
from torchvision import models
from sklearn.metrics import confusion_matrix
import numpy as np
from numpy.typing import NDArray
from torch.utils.data import DataLoader
from torch._prims_common import DeviceLikeType
from sklearn.metrics import ConfusionMatrixDisplay
from torchvision.datasets import ImageFolder
import matplotlib.pyplot as plt
# stdlib
from glob import glob
import argparse
from pathlib import PurePath


def get_confusion_matrix(
        model: torch.nn.Module,
        validation_loader: DataLoader,
        device: DeviceLikeType) -> NDArray:
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for inputs, labels in validation_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            all_preds.append(predicted.cpu().numpy())
            all_labels.append(labels.cpu().numpy())

    # Convert list of arrays to single numpy arrays
    all_preds = np.concatenate(all_preds)
    all_labels = np.concatenate(all_labels)

    # Print the shape of preds and labels
    print(f"Number of predictions: {len(all_preds)}")
    print(f"Number of true labels: {len(all_labels)}")
    # Compute the confusion matrix
    conf_matrix = confusion_matrix(all_labels, all_preds)
    return conf_matrix


def display_confusion_matrix(
    model: torch.nn.Module,
    validation_loader: DataLoader,
    classes: list[str],
    device: DeviceLikeType
):
    print("Generating confusion matrix")
    # Display the confusion matrix
    conf_matrix = get_confusion_matrix(model, validation_loader, device)

    disp = ConfusionMatrixDisplay(
        confusion_matrix=conf_matrix, display_labels=classes)
    disp.plot(cmap=plt.cm.Blues)
    plt.show()


if __name__ == "__main__":
    # locals
    from transform_images import get_validation_transforms
    from model_state import load_model_from_disk
    # this is for if you want to display a confusion matrix
    # for an existing model
    parser = argparse.ArgumentParser(
        description="Train the tree recognition model")
    parser.add_argument("--model", nargs="?", const=None, type=str,
                        help="Filename of the model you want to use")
    parser.add_argument("--image-size", nargs="?", const=256, default=256,
                        type=int, help="Size of the validation images")
    parser.add_argument("--validation-folder", nargs="?",
                        const="trees_valuation", default="trees_valuation",
                        type=str, help="The folder with validation images")
    args = parser.parse_args()

    validation_data = ImageFolder(
        root=args.validation_folder,
        transform=get_validation_transforms(args.image_size)
    )
    validation_loader = DataLoader(
        validation_data, batch_size=32, shuffle=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    class_names = [
        PurePath(path).name
        for path in glob("trees_training/resized/*")
    ]

    # initialize the model
    model = models.resnet34(weights=None)
    model.fc = torch.nn.Linear(model.fc.in_features, len(class_names))
    load_model_from_disk(model)
    model = model.to(device)  # Move model to device

    display_confusion_matrix(model, validation_loader, class_names, device)
