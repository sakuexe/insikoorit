import torch
from torch import nn
import os


DEFAULT_MODEL = "best_model_weights.pth"
WEIGHTS_ROOT = "weights"


def save_model_to_disk(
    model: nn.Module,
    weights_root=WEIGHTS_ROOT,
    model_name=DEFAULT_MODEL,
    extra_info=""
) -> None:
    """Saves the model passed to the function into a weights
    file on the disk inside the provided weights root folder
    """
    save_filepath = os.path.join(weights_root, model_name)

    try:
        if not os.path.exists(weights_root):
            os.mkdir(weights_root)
    except OSError as err:
        print(f"Could not create folder: {weights_root}")
        print("Either create the folder yourself or fix the issue")
        print(f"Error: \n{err}")

    try:
        torch.save(model.state_dict(), save_filepath)
    except OSError as err:
        print("Could save model to disk")
        print(f"Error: \n{err}")

    print(f"Model saved successfully! {extra_info}")


def load_model_from_disk(
    model: nn.Module,
    weights_root=WEIGHTS_ROOT,
    model_name=DEFAULT_MODEL,
):
    load_filepath = os.path.join(weights_root, model_name)
    if not os.path.exists(load_filepath):
        raise OSError(f"No weights file was found in path: {load_filepath}")
    model.load_state_dict(torch.load(load_filepath, weights_only=True))
