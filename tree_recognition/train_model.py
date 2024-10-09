# pytorch
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision.transforms import Compose, Resize, ToTensor
from torch.utils.tensorboard.writer import SummaryWriter
from torchsummary import summary
# visualization
from PIL import Image
import matplotlib.pyplot as plt
# stdlib
import os
import random
import argparse
import glob
# local
from training_fn import train_model, validate_model
from utils.model_state import save_model_to_disk, load_model_from_disk

TRAINING_ROOT = "trees_training/edited"
VALIDATION_ROOT = "trees_valuation"
LEARNING_RATE = 0.01
EPOCHS = 10
IMAGE_RESIZE = 128

parser = argparse.ArgumentParser(
    description="Train the tree recognition model")
parser.add_argument("--run-name", nargs="?", type=str,
                    help="The folder name of the logs in runs/")
parser.add_argument("--learning-rate", nargs="?", type=float,
                    help="The learning rate")
parser.add_argument("--epochs", nargs="?", type=int,
                    help="Number of iterations")
parser.add_argument("--image-size", nargs="?", type=int,
                    help="Size of the images given to the model to train on")
parser.add_argument("--verbose", action="store_true",
                    help="Print more info about the model during training")
parser.add_argument("--continue-training", nargs="?",
                    const=True, default=False, type=str,
                    help="Load the saved model instead of starting from \
                    scratch")
args = parser.parse_args()

LEARNING_RATE = args.learning_rate or LEARNING_RATE
EPOCHS = args.epochs or EPOCHS
IMAGE_RESIZE = args.image_size or IMAGE_RESIZE

# use gpu if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if args.verbose:
    print(f"The current device is: {device}")

# tensorboard writer
number_of_runs = len(glob.glob("runs/*"))
folder_name = args.run_name or f"trees_{number_of_runs}"
writer = SummaryWriter(f"runs/{folder_name}")

# load and preprocess the dataset

# transformations, like resizing
transform = Compose([Resize((IMAGE_RESIZE, IMAGE_RESIZE)), ToTensor()])
# load the dataset
train_data = ImageFolder(root=TRAINING_ROOT, transform=transform)
validation_data = ImageFolder(root=VALIDATION_ROOT, transform=transform)

if args.verbose:
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
# input size and output size
model.fc = nn.Linear(512, len(train_data.classes)).to(device)
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

if args.verbose:
    # display a detailed summary of the model's architecture
    # the ResNet34 and ResNet18 use a input size of 224, 224
    summary(model, input_size=(3, 224, 224))
    print("current model: resnet34")
    print(model)

if args.continue_training is True:
    print("continuing training on an existing model")
    load_model_from_disk(model)
elif args.continue_training:
    print("continuing training on an existing model")
    load_model_from_disk(model, model_name=args.continue_training)

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
    writer.add_scalar('Accuracy/train', training_data["epoch_accuracy"], epoch)
    writer.add_scalar('Loss/validation', validation_data["epoch_loss"], epoch)
    writer.add_scalar('Accuracy/validation',
                      validation_data["epoch_accuracy"],
                      epoch)

    # save the model whenever validation loss is lower than the previous best
    if validation_data["epoch_loss"] < best_validation_loss:
        best_validation_loss = validation_data["epoch_loss"]
        save_model_to_disk(model)
