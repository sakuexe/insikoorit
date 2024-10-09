import torch
import torch.nn as nn


class TreeCNN(nn.Module):
    def __init__(self, classes, image_size):
        super(TreeCNN, self).__init__()
        # get the size that fc1 and x.view need
        self.convoluted_filesize = int((image_size / 2) / 2)
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(32 * self.convoluted_filesize * self.convoluted_filesize, image_size)
        self.fc2 = nn.Linear(image_size, len(classes))  # Number of classes

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        # Flattening the tensor for the fully connected layers
        x = x.view(-1, 32 * self.convoluted_filesize * self.convoluted_filesize)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x
