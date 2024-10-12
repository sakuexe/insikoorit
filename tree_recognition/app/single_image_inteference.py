import torch
import torch.nn.functional as F
from torchvision.transforms import Compose, Resize, ToTensor
from torchvision import models
from PIL import Image
from model_state import load_model_from_disk
from dataclasses import dataclass

WEIGHTS_ROOT = "weights"
DEFAULT_MODEL = "best_model_weights.pth"
IMAGE_RESIZE = 1080
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


@dataclass
class Probability:
    class_name: str
    confidence: float


@dataclass
class InferenceResult:
    prediction: str
    confidence: float
    probabilities: list[Probability]


def infer_single_image(
    model: torch.nn.Module,
    image_path: str,
    transform: Compose,
    classes: list[str]
) -> InferenceResult:
    # Load and preprocess the image
    image = Image.open(image_path).convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0)  # Add batch dimension

    # Move to device
    image = image.to(DEVICE)

    # debug tensor shape if issues
    # print(f"Input tensor shape: {image.shape}")

    # Forward pass
    with torch.no_grad():
        output = model(image)
        probabilities = F.softmax(output, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
        predicted_class = classes[predicted.item()]

        all_probabilities: list[Probability] = []
        for index, prob in enumerate(probabilities[0]):
            probability = Probability(classes[index], round(prob.item(), 3))
            all_probabilities.append(probability)

    all_probabilities.sort(key=lambda x: x.confidence, reverse=True)
    return InferenceResult(
        predicted_class,
        confidence.item(),
        all_probabilities
    )


def generate_infer(
    image_path: str,
    model_name=DEFAULT_MODEL
) -> InferenceResult:
    # get the classes dynamically based on the amount of folders
    # inside the training root
    class_names = ['birch', 'juniper', 'linden',
                   'maple', 'oak', 'pine', 'rowan', 'spruce']

    # load the model
    model = models.resnet34(weights=None)
    model.fc = torch.nn.Linear(model.fc.in_features, len(class_names))
    load_model_from_disk(model, weights_root=WEIGHTS_ROOT,
                         model_name=model_name)
    model = model.to(DEVICE)  # Move model to device
    model.eval()

    # define transform
    transform = Compose([
        Resize((IMAGE_RESIZE, IMAGE_RESIZE)),
        ToTensor()
    ])

    return infer_single_image(
        model,
        image_path,
        transform,
        class_names
    )
