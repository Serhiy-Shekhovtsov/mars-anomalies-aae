"""Utils.
"""
import torch
import matplotlib
import matplotlib.cm
from PIL import Image, ContainerIO
import pvl


def extract_img(image_file: str) -> Image:
    """Extracts and returns embedded image from PDS3 IMG files as PIL Image.

    Args:
        image_file (str): path to .IMG file.

    Returns:
        PIL.Image
    """

    # Parsing label
    label = pvl.load(image_file)  # load label from .IMG file
    image_data = label['IMAGE']  # getting image object info

    h_img, w_img = image_data[0][-1], image_data[1][-1]  # real image sizes
    pref, suff = image_data[6][-1], image_data[7][-1]  # buffer pixels margins
    w_total = w_img + pref + suff  # width with margins

    offset = label['^IMAGE'].value  # pointer where image is located
    size = label['^GAP_TABLE'].value - label['^IMAGE'].value  # image size (in bytes)

    # Now getting back to file
    with open(image_file, "rb") as f:
        container = ContainerIO.ContainerIO(f, offset - 1, size)
        data = container.read()  # reading image bytes
        img = Image.frombytes('L', (w_total, h_img), data, "raw")  # decoding
        img = img.crop((pref, 0, w_img + pref, h_img))  # cropping margins

    return img


def colorize_img(img, vmin=None, vmax=None, cmap='gray'):
    """
    Based on https://gist.github.com/jimfleming/c1adfdb0f526465c99409cc143dea97b#gistcomment-2398882
    A utility function for Torch/Numpy that maps a grayscale image to a matplotlib
    colormap for use with TensorBoard image summaries.
    By default it will normalize the input value to the range 0..1 before mapping to a grayscale colormap.

    Args:
      img: 2D Tensor of shape [height, width] or 3D Tensor of shape [height, width, 1].
      vmin: the minimum value of the range used for normalization. (Default: value minimum)
      vmax: the maximum value of the range used for normalization. (Default: value maximum)
      cmap: a valid cmap named for use with matplotlib's `get_cmap`. (Default: Matplotlib default colormap)

    Returns a 4D tensor of shape [height, width, 4].
    """
    # normalize
    vmin = img.min() if vmin is None else vmin
    vmax = img.max() if vmax is None else vmax

    if vmin != vmax:
        img = (img - vmin) / (vmax - vmin)  # vmin..vmax
    else:
        # Avoid 0-division
        img = img * 0.

    # squeeze last dim if it exists
    img = img.squeeze()

    cmapper = matplotlib.cm.get_cmap(cmap)

    img = cmapper(img, alpha=None, bytes=False)  # RGBA | HWC (C=4)
    tensor_img = torch.tensor(img)  # CHW (C=3)

    return tensor_img


def colorize_batch(batch, **kwargs):
    """Colorizes batch of images.

    Args:
        batch (torch.tensor): torch minibatch of images of shape (BCHW)

    Returns:
         4D torrch tensor of shape BCHW
    """
    colorized = torch.stack([colorize_img(img, **kwargs)[:, :, :3].transpose(2, 0) for img in batch])

    return colorized
