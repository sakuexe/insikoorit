import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard.writer import SummaryWriter
from typing import Callable
import os

WEIGHTS_ROOT = "weights"


def train_model(
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        loss_fn: Callable,
        optimizer: torch.optim.SGD | torch.optim.Adam,
        writer: SummaryWriter,
        num_epochs=10):

    best_val_loss = float('inf')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # make sure that the directory for the trained data exists
    if not os.path.exists(WEIGHTS_ROOT):
        os.makedirs(WEIGHTS_ROOT)

    for epoch in range(num_epochs):
        running_train_loss = 0.0
        model.train()
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()
            running_train_loss += loss.item()

        train_loss = running_train_loss / len(train_loader)

        # Validation
        running_val_loss = 0.0
        correct = 0
        total = 0
        model.eval()
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = loss_fn(outputs, labels)
                running_val_loss += loss.item()

                # Calculate validation accuracy
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        val_loss = running_val_loss / len(val_loader)
        val_accuracy = 100 * correct / total

        print(f"""Epoch [{epoch+1}/{num_epochs}], Train Loss: {train_loss:.4f},
        Val Loss: {val_loss:.4f}, Val Accuracy: {val_accuracy:.2f}%""")

        # Log losses and accuracy to TensorBoard
        writer.add_scalar('Loss/train', train_loss, epoch)
        writer.add_scalar('Loss/validation', val_loss, epoch)
        writer.add_scalar('Accuracy/validation', val_accuracy, epoch)

        # Save the best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            save_filepath = f"{WEIGHTS_ROOT}/best_model_weights.pth"
            torch.save(model.state_dict(), save_filepath)
            print(f"Model saved at epoch {epoch+1}")

    writer.close()
