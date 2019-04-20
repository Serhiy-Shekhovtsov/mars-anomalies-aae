import numpy as np
import torch
import torch.nn as nn


def numpy_images_to_tensor_dataset(images):
    """Converts list of images to PyTorch tensor"""

    # creating big nd array from array of arrrays
    images_matrix = np.stack(images)

    # convert to tensor with dimentions B x H x W x C
    # converting to float required by PyTorch
    tensor_images = torch.from_numpy(images_matrix).float()

    # make the color channel dimension second instead of last
    # new dimentions will be B x C x H x W
    tensor_images = tensor_images.permute(0, 3, 1, 2)

    return tensor_images

def get_current_device():
    try:
        # we need it because of cuda bug:
        # https://github.com/pytorch/pytorch/issues/17108
        _ = torch.cuda.current_device()
    except:
        pass

    # Device configuration
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    return device

class Flatten(nn.Module):
    def forward(self, x):
        N, C, H, W = x.size() # read in N, C, H, W
        return x.view(N, -1)  # "flatten" the C * H * W values into a single vector per image
    
class Unflatten(nn.Module):
    """
    An Unflatten module receives an input of shape (N, C*H*W) and reshapes it
    to produce an output of shape (N, C, H, W).
    """
    def __init__(self, N=-1, C=20, H=16, W=16):
        super(Unflatten, self).__init__()
        self.N = N
        self.C = C
        self.H = H
        self.W = W
        
    def forward(self, x):
        return x.view(self.N, self.C, self.H, self.W)
