import numpy as np
from PIL import Image, ContainerIO
import pvl
import matplotlib.pyplot as plt
from collections.abc import Iterable


def extract_img(image_file: str):
    """Extracts and returns embedded image from PDS3 IMG files as PIL Image"""
    
    # Parsing label
    label = pvl.load(image_file)  # load label from .IMG file
    image_data = label['IMAGE']   # getting image object info
    h_img, w_img = image_data[0][-1], image_data[1][-1]  # real image sizes
    pref, suff = image_data[6][-1], image_data[7][-1]    # buffer pixels margins
    w_total = w_img + pref + suff                        # width with margins

    offset = label['^IMAGE'].value  # pointer where image is located
    size = label['^GAP_TABLE'].value - label['^IMAGE'].value  # image size (in bytes)
    
    # Now getting back to file
    with open(image_file, "rb") as f:
        container = ContainerIO.ContainerIO(f, offset-1, size)
        data = container.read()  # reading image bytes
        img = Image.frombytes('L', (w_total, h_img), data, "raw")  # decoding
        img = img.crop((pref, 0, w_img + pref, h_img))  # cropping margins
    
    return img


def get_patch_indexes(img_size, patch_size):
    patches_n = img_size / patch_size
    remainder = img_size % patch_size
    
    # get list of full patches
    indexes = list(range(0, int(patches_n)))
    
    # last patch will start from the end of previous and to the end of the image
    if remainder:
        indexes.append(patches_n - 1)
    
    return [int(i * patch_size) for i in indexes]


def extract_patches(src_img, patch_size):
    img_height = src_img.shape[0]
    img_width = src_img.shape[1]

    h_indexes = get_patch_indexes(img_height, patch_size)
    w_indexes = get_patch_indexes(img_width, patch_size)

    patches = np.zeros((len(h_indexes), len(w_indexes)), dtype=object)

    for h_i, h in enumerate(h_indexes):    
        for w_i, w in enumerate(w_indexes):
            patch = src_img[h: h+patch_size, w: w+patch_size, :]

            patches[h_i, w_i] = patch
    
    return patches


def get_patches_ids(patches, id_prefix=''):
    ids = []
    
    for i in range(0, patches.shape[0]):    
        for j in range(0, patches.shape[1]):
            ids.append(f'{id_prefix}_{i}_{j}')
    
    return patches.flatten(), ids


def extract_patches_from_img(img_name, patch_size=256):
    """Reads IMG file, parses it and split into patches of specified size
    
    Args:
        img_name (str or list of strings): list of images to extract patches from
        patch_size (int, optional): Defaults to 256. [description]
    
    Returns:
        list: patches from all files
        list: unique ids for all patches
    """

    img_names = img_name if type(img_name) == list else [img_name]
    all_images = []
    all_ids = []

    for img_name in img_names:
        sample_img = np.asarray(extract_img(f'data/{img_name}'))

        # images having 1000 height are corrupted
        if sample_img.shape[0] == 1000:
            # skipping corrupted image
            continue

        sample_img = sample_img[..., np.newaxis]

        patches = extract_patches(sample_img, patch_size=patch_size)
        images, ids = get_patches_ids(patches, img_name)

        all_images += images.tolist()
        all_ids += ids

    return all_images, all_ids
