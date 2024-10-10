import torch
from torchvision.transforms import Compose, Resize, ToTensor
from torchvision.datasets import ImageFolder
from torchvision import models
from PIL import Image
from utils.model_state import load_model_from_disk
import torch.nn.functional as F


WEIGHTS_ROOT = "weights"
DEFAULT_MODEL = "best_model_weights.pth"
IMAGE_RESIZE = 128
NUM_CLASSES = 8
TRAINING_ROOT = "trees_training/resized"  # Path to the training dataset

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def infer_single_image(model, image_path, transform, classes):
    # Load and preprocess the image
    image = Image.open(image_path).convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0)  # Add batch dimension

    # Move to device
    image = image.to(device)

    # debug tensor shape if issues
    # print(f"Input tensor shape: {image.shape}")


    # Forward pass
    with torch.no_grad():
        output = model(image)
        probabilities = F.softmax(output, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
        predicted_class = classes[predicted.item()]
    return predicted_class, confidence.item()

    
# Dynamically get the class names from the training dataset
train_dataset = ImageFolder(root=TRAINING_ROOT, transform=Compose([
    Resize((IMAGE_RESIZE, IMAGE_RESIZE)),
    ToTensor()
]))

class_names = train_dataset.classes
NUM_CLASSES = len(class_names)

#debug
print(f"Number of classes: {NUM_CLASSES}")
print(f"Class names: {class_names}")


model = models.resnet34(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, NUM_CLASSES)
load_model_from_disk(model, weights_root=WEIGHTS_ROOT, model_name=DEFAULT_MODEL)
model = model.to(device)  # Move model to device
model.eval()

# define transform
transform = Compose([
    Resize((IMAGE_RESIZE, IMAGE_RESIZE)),
    ToTensor()
])

# image_path, take input aswell later?
image_path = 'trees_valuation/birch/birch_004.jpg'

predicted_class, confidence = infer_single_image(model, image_path, transform, class_names)

print(f"Predicted class: {predicted_class}\nConfidence: {confidence}")

