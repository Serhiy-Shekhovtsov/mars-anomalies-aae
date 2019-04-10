import numpy as np


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
            patch = src_img[h : h+patch_size, w : w+patch_size, :]

            patches[h_i, w_i] = patch
    
    return patches

def get_patches_ids(patches, id_prefix = ''):
    ids = []
    
    for i in range(0, patches.shape[0]):    
        for j in range(0, patches.shape[1]):
            ids.append(f'{id_prefix}_{i}_{j}')
    
    return patches.flatten(), ids
