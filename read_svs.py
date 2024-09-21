from matplotlib import pyplot as plt
import numpy as np
import os
import tqdm

# The path can also be read from a config file, etc.
OPENSLIDE_PATH = 'C:/Users/tkalr/Downloads/openslide-bin-4.0.0.5-windows-x64/bin'

if hasattr(os, 'add_dll_directory'):
    # Windows
    with os.add_dll_directory(OPENSLIDE_PATH):
        import openslide
        from openslide import open_slide
else:
    import openslide
    from openslide import open_slide

save = True

dir_img = 'C:/Users/tkalr/OneDrive/Desktop/Documents/Projects/svs/WSI'
valid_images = ['.svs']
patch_size = (2000, 2000)

for f in tqdm.tqdm(os.listdir(dir_img)):
    ext = os.path.splitext(f)[0]
    if ext != 'JP2K-33003-1':
        continue
    curr_path = os.path.join(dir_img, f)
    print(curr_path)

    # open scan
    scan = openslide.OpenSlide(curr_path)

    # Try to get dimensions from properties, fall back to scan.dimensions if not found
    orig_w = scan.properties.get('aperio.OriginalWidth')
    orig_h = scan.properties.get('aperio.OriginalHeight')

    if orig_w is None or orig_h is None:
        orig_w, orig_h = scan.dimensions  # Fallback to dimensions

    orig_w = np.int64(orig_w)
    orig_h = np.int64(orig_h)

    # create an array to store our image
    img_np = np.zeros((orig_w, orig_h, 3), dtype=np.uint8)

    for r in range(0, orig_w, patch_size[0]):
        for c in range(0, orig_h, patch_size[1]):
            if c + patch_size[1] > orig_h and r + patch_size[0] <= orig_w:
                p = orig_h - c
                img = np.array(scan.read_region((c, r), 0, (p, patch_size[1])), dtype=np.uint8)[..., 0:3]
            elif c + patch_size[1] <= orig_h and r + patch_size[0] > orig_w:
                p = orig_w - r
                img = np.array(scan.read_region((c, r), 0, (patch_size[0], p)), dtype=np.uint8)[..., 0:3]
            elif c + patch_size[1] > orig_h and r + patch_size[0] > orig_w:
                p = orig_h - c
                pp = orig_w - r
                img = np.array(scan.read_region((c, r), 0, (p, pp)), dtype=np.uint8)[..., 0:3]
            else:
                img = np.array(scan.read_region((c, r), 0, (patch_size[0], patch_size[1])), dtype=np.uint8)[..., 0:3]
            img_np[r:r + patch_size[0], c:c + patch_size[1]] = img

    if save:
        name_no_ext = os.path.splitext(f)[0]
        np.save(os.path.join(dir_img, name_no_ext), img_np)

    scan.close()
