import torch
from torch._prims_common import DeviceLikeType
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Callable, TypedDict



class TrainingData(TypedDict):
    """Typed dictionary for passing the epoch data for"""
    epoch_loss: float
    epoch_accuracy: float


def train_model(
        model: nn.Module,
        train_loader: DataLoader,
        loss_fn: Callable,
        optimizer: torch.optim.SGD | torch.optim.Adam,
        device: DeviceLikeType) -> TrainingData:

    model.train()
    running_loss, total, correct = (0, 0, 0)

    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        # Forward pass
        outputs = model(inputs)
        loss = loss_fn(outputs, labels)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    epoch_loss = running_loss / len(train_loader)
    epoch_accuracy = 100. * correct / total

    print(f"Train Loss: {epoch_loss}, Train Accuracy: {epoch_accuracy}%")

    epoch_data: TrainingData = {
        "epoch_loss": float(epoch_loss),
        "epoch_accuracy": epoch_accuracy
    }
    return epoch_data


def validate_model(
        model: nn.Module,
        validation_loader: DataLoader,
        loss_fn: Callable,
        device: DeviceLikeType) -> TrainingData:

    model.eval()
    running_loss, correct, total = (0, 0, 0)

    with torch.no_grad():
        for inputs, labels in validation_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            # Forward pass
            outputs = model(inputs)
            loss = loss_fn(outputs, labels)

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

    epoch_loss = running_loss / len(validation_loader)
    epoch_accuracy = 100. * correct / total

    print(f"Validation Loss: {epoch_loss}, \
    Validation Accuracy: {epoch_accuracy}%")

    epoch_data: TrainingData = {
        "epoch_loss": float(epoch_loss),
        "epoch_accuracy": epoch_accuracy
    }
    return epoch_data
