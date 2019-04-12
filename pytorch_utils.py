import numpy as np
import torch

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
