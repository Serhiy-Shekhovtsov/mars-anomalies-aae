import torch
import torch.nn as nn


class ConvAutoencoderV1(nn.Module):
    def __init__(self, image_channels=1):
        super(ConvAutoencoderV1, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(image_channels, 100, kernel_size=5, stride=1, padding=2), # 100 5x5 filters. padding = 'same'
            nn.ReLU(),
            nn.MaxPool2d(2, stride=2),
            nn.Conv2d(100, 200, kernel_size=5, stride=1, padding=2), # 200 5x5 filters. padding = 'same'
            nn.ReLU(),
            nn.MaxPool2d(2, stride=2),
        )
        
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(200, 100, kernel_size=4, stride=2, padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(100, 1, kernel_size=4, stride=2, padding=1),
            nn.Sigmoid(),
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x