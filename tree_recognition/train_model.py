import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision.transforms import Compose, Resize, ToTensor
from torch.utils.tensorboard.writer import SummaryWriter
from PIL import Image
import matplotlib.pyplot as plt
import os
import random
from cnn_model import TreeCNN
from training_fn import WEIGHTS_ROOT, train_model

TRAINING_ROOT = "trees_training/edited"
VALIDATION_ROOT = "trees_valuation"
LEARNING_RATE = 0.01
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
    print(f"filenames in {dirpath} are: {filenames}")
    filepath = os.path.join(dirpath, random.choice(filenames))
    image_paths.append(filepath)
    titles.append(os.path.basename(os.path.normpath(dirpath)))

# Load the images
images = [Image.open(image_path) for image_path in image_paths]

# display the images
fig, axs = plt.subplots(1, len(images), figsize=(12, 5))
for ax, image, title in zip(axs, images, titles):
    ax.imshow(image)
    ax.axis("off")  # Hide axis ticks
    ax.set_title(title)

plt.tight_layout()
plt.show()

# initialize the model
model = TreeCNN(train_data.classes, IMAGE_RESIZE).to(device)
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=LEARNING_RATE, momentum=0.9)

train_model(model,
            train_loader,
            validation_loader,
            loss_fn,
            optimizer,
            writer,
            num_epochs=10)

# load the best model for inference
model.load_state_dict(torch.load(f'{WEIGHTS_ROOT}/best_model_weights.pth'))
model.eval()
