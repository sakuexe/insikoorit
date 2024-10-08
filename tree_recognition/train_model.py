import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision.transforms import Compose, Resize, ToTensor
from torch.utils.tensorboard.writer import SummaryWriter
from torchsummary import summary
from PIL import Image
import matplotlib.pyplot as plt
import os
import random
from training_fn import train_model, validate_model
from utils.save_model import save_model_to_disk

TRAINING_ROOT = "trees_training/edited"
VALIDATION_ROOT = "trees_valuation"
LEARNING_RATE = 0.01
EPOCHS = 10
IMAGE_RESIZE = 128

# use gpu if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# tensorboard writer
writer = SummaryWriter('runs/trees_experiment')

# load and preprocess the dataset

# transformations, like resizing
transform = Compose([Resize((IMAGE_RESIZE, IMAGE_RESIZE)), ToTensor()])
# load the dataset
train_data = ImageFolder(root=TRAINING_ROOT, transform=transform)
validation_data = ImageFolder(root=VALIDATION_ROOT, transform=transform)

print("Classes from training data are:", train_data.classes)

# Create data loaders
train_loader = DataLoader(train_data, batch_size=16, shuffle=True)
validation_loader = DataLoader(validation_data, batch_size=16, shuffle=True)

# Display random images from each dataset
image_paths = []
titles = []
for dirpath, _, filenames in os.walk(TRAINING_ROOT):
    if not filenames:
        continue
    filepath = os.path.join(dirpath, random.choice(filenames))
    image_paths.append(filepath)
    titles.append(os.path.basename(os.path.normpath(dirpath)))

# Load the images
images = [Image.open(image_path) for image_path in image_paths]

# display a random sample of each class
fig, axs = plt.subplots(1, len(images), figsize=(12, 5))
for ax, image, title in zip(axs, images, titles):
    ax.imshow(image)
    ax.axis("off")  # Hide axis ticks
    ax.set_title(title)

plt.tight_layout()
plt.show()

# initialize the model
model = models.resnet34(weights=models.ResNet34_Weights.DEFAULT).to(device)
# display a detailed summary of the model's architecture
# the ResNet34 and ResNet18 use a input size of 224, 224
summary(model, input_size=(3, 224, 224))
print(model)

# input size and output size
model.fc = nn.Linear(512, len(train_data.classes)).to(device)
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

best_validation_loss = float('inf')

for epoch in range(EPOCHS):
    print(f"Epoch {epoch+1}/{EPOCHS}")
    training_data = train_model(
        model,
        train_loader,
        loss_fn,
        optimizer,
        device,
    )
    validation_data = validate_model(
        model,
        validation_loader,
        loss_fn,
        device,
    )

    # Log losses and accuracy to TensorBoard
    writer.add_scalar('Loss/train', training_data["epoch_loss"], epoch)
    writer.add_scalar('Loss/validation', validation_data["epoch_loss"], epoch)
    writer.add_scalar('Accuracy/validation',
                      validation_data["epoch_accuracy"],
                      epoch)

    # save the model whenever validation loss is lower than the previous best
    if validation_data["epoch_loss"] < best_validation_loss:
        best_val_loss = validation_data["epoch_loss"]
        save_model_to_disk(model)
