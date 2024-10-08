import torch
from torch import nn
import os


def save_model_to_disk(
    model: nn.Module,
    WEIGHTS_ROOT="weights",
    model_name="best_model_weights",
    extra_info=""
) -> None:
    """Saves the model passed to the function into a weights
    file on the disk inside the provided weights root folder
    """
    save_filepath = os.path.join(WEIGHTS_ROOT, f"{model_name}.pth")

    try:
        if not os.path.exists(WEIGHTS_ROOT):
            os.mkdir(WEIGHTS_ROOT)
    except OSError as err:
        print(f"Could not create folder: {WEIGHTS_ROOT}")
        print("Either create the folder yourself or fix the issue")
        print(f"Error: \n{err}")

    try:
        torch.save(model.state_dict(), save_filepath)
    except OSError as err:
        print("Could save model to disk")
        print(f"Error: \n{err}")

    print(f"Model saved successfully! {extra_info}")
