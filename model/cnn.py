import torch.nn as nn
from torch import Tensor


class CNN(nn.Module):
    def __init__(self, num_class=62, num_char=4):
        super(CNN, self).__init__()
        self.num_class = num_class
        self.num_char = num_char
        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=(1, 1)),
            nn.MaxPool2d(2, 2),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.Conv2d(16, 32, 3, padding=(1, 1)),
            nn.MaxPool2d(2, 2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, 3, padding=(1, 1)),
            nn.MaxPool2d(2, 2),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 128, 3, padding=(1, 1)),
            nn.MaxPool2d(2, 2),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 256, 3, padding=(1, 1)),
            nn.MaxPool2d(2, 2),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Dropout(p=0.5, inplace=False),
        )
        self.fc = nn.Linear(256 * 6 * 1, self.num_class * self.num_char)

    def forward(self, x: Tensor) -> Tensor:
        x = self.conv(x)
        x = x.view(-1, 256 * 6 * 1)
        x = self.fc(x)
        return x
