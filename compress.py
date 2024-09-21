import os
import numpy as np
import torch
from PIL import Image
from compressai.utils.bench.codecs import compute_metrics
import timeit
import tqdm
from models import *
from ranges import *
from sizes import *

def pad_image(image, tile_size):
    """Pad the image so its dimensions are divisible by the tile size."""
    img_h, img_w, _ = image.shape
    pad_h = (tile_size[0] - img_h % tile_size[0]) % tile_size[0]
    pad_w = (tile_size[1] - img_w % tile_size[1]) % tile_size[1]
    padded_image = np.pad(image, ((0, pad_h), (0, pad_w), (0, 0)), mode='constant', constant_values=0)
    return padded_image, pad_h, pad_w

def patch_image(image, patch_size=(1024, 1024)):
    patches = []
    img_h, img_w, _ = image.shape
    for y in range(0, img_h, patch_size[1]):
        for x in range(0, img_w, patch_size[0]):
            patch = image[y:y + patch_size[1], x:x + patch_size[0], :]
            patches.append(patch)
    return patches

def process(name , model , image_folder = 'samples/inputs' , output_folder = 'samples/outputs' , patch_size = (1024, 1024)):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(image_folder):
        if filename.endswith(".npy"):
            #Load .npy file created from the .svs file
            image_path = os.path.join(image_folder, filename)
            img = np.load(image_path)

            padded_img, pad_h, pad_w = pad_image(img, patch_size)

            #Make patches
            patches = patch_image(padded_img, patch_size)

            #Compress each patch individually
            for i, patch in enumerate(patches):
                
                patch_Folder = output_folder + f'/{name}_{filename.split('.')[0]}_original'
                if not os.path.exists(patch_Folder):
                    os.makedirs(patch_Folder)
                patch_PATH = patch_Folder + f'/patch_{i}.png'
                Image.fromarray(patch).save(patch_PATH)

                # Convert patch data to tensor
                patch = torch.from_numpy(patch).permute(2, 0, 1).unsqueeze(0).float() / 255.0
                
                with torch.no_grad():
                    compressed = model.compress(patch)
                with torch.no_grad():
                    decompressed = model.decompress(compressed['strings'], compressed['shape'])
                
                decompressed_patch = decompressed['x_hat'].squeeze(0).permute(1, 2, 0).clamp(0, 1) * 255
                decompressed_patch = decompressed_patch.byte().numpy()
                
                patch_np = patch.squeeze(0).permute(1, 2, 0).numpy()
                decompressed_np = decompressed['x_hat'].squeeze(0).permute(1, 2, 0).numpy()
                metrics = compute_metrics(decompressed_np, patch_np, metrics=["psnr-rgb", "ms-ssim-rgb"])
                
                NEW_patch_FOLDER = os.path.join(output_folder, f'{name}_{filename.split('.')[0]}')
                if not os.path.exists(NEW_patch_FOLDER):
                    os.makedirs(NEW_patch_FOLDER)
                NEW_patch_PATH = os.path.join(NEW_patch_FOLDER , f'patch_{i}.png')
                Image.fromarray(decompressed_patch).save(NEW_patch_PATH)
                result_file = os.path.join(output_folder, f'outputs_{name}_{filename.split('.')[0]}.txt')
                with open(result_file, 'a') as f:
                    f.write(f"Model : {name}\n")
                    f.write(f"Filename : {filename} (patch {i})\n")
                    f.write(f"PSNR: {metrics['psnr-rgb']:.4f}\n")
                    f.write(f"MS-SSIM: {metrics['ms-ssim-rgb']:.4f}\n\n")
        return [result_file , patch_Folder , NEW_patch_FOLDER]

if __name__ == "__main__":
    
    out_file = 'samples/output.txt'
    image_folder = 'samples/inputs'
    output_folder = 'C:/Users/tkalr/OneDrive/Desktop/Documents/Projects/compression/samples/outputs'

    for i in range(1,3):
        start = timeit.default_timer()
        
        models = get_model(str(i))
        filename , original , compressed = process(models['name'] , models['model'] , image_folder , output_folder)
        
        stop = timeit.default_timer()
        
        psnr_range, ms_ssim_range = find_range(filename)
        min_diff , max_diff = find_sizes(original , compressed)

        with open(out_file , 'a') as f:
            f.write(f'Model : {models['name']}\n')
            f.write(f'Time : {stop-start}\n')
            f.write(f'PSNR Range : {psnr_range}\n')
            f.write(f'MS-SSIM Range : {ms_ssim_range}\n')
            f.write(f'Minimum compression in size(for a patch) : {min_diff}\n')
            f.write(f'Maximum compression in size(for a patch) : {max_diff}\n\n')