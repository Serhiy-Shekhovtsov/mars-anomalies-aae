import matplotlib.pyplot as plt
from matplotlib.image import imread

from extract_patches import *

# as an example I used the photo of Great Horned Owl. © Patricia Velte 
owl_img = imread('examples/owl.jpg')

patches = extract_patches(owl_img, patch_size=200)

fig, img_plots = plt.subplots(*patches.shape, figsize=(8, 10), gridspec_kw = {'wspace':0.05, 'hspace':0.05})

fig.patch.set_facecolor('black')

for i in range(0, patches.shape[0]):    
    for j in range(0, patches.shape[1]):
        img_plt = img_plots[i, j]
        
        img_plt.imshow(patches[i, j])        
        img_plt.axis('off')
        
plt.subplots_adjust(wspace=0, hspace=0, left=0, right=1, bottom=0, top=1)
plt.show()

patches_list, ids = get_patches_ids(patches, 'test')

print(ids)

plt.imshow(patches_list[1])
plt.show()

plt.imshow(patches_list[7])
plt.show()
