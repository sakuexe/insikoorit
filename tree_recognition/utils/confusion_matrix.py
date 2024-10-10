import torch
from sklearn.metrics import confusion_matrix
import numpy as np
from numpy.typing import NDArray
from torch.utils.data import DataLoader
from torch._prims_common import DeviceLikeType

# Function to get predictions for the entire validation set


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
