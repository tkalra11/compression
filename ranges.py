import re

def parse_metrics_from_file(filename):
    psnr_values = []
    ms_ssim_values = []

    psnr_pattern = r'PSNR:\s*([\d.]+)'
    ms_ssim_pattern = r'MS-SSIM:\s*([\d.]+)'
    
    with open(filename, 'r') as file:
        for line in file:
            psnr_match = re.search(psnr_pattern, line)
            ms_ssim_match = re.search(ms_ssim_pattern, line)
            
            if psnr_match:
                psnr_values.append(float(psnr_match.group(1)))
            if ms_ssim_match:
                ms_ssim_values.append(float(ms_ssim_match.group(1)))
    
    return psnr_values, ms_ssim_values

def find_range(filename):
    psnr_values, ms_ssim_values = parse_metrics_from_file(filename)
    psnr_range = (min(psnr_values), max(psnr_values)) if psnr_values else (None, None)
    ms_ssim_range = (min(ms_ssim_values), max(ms_ssim_values)) if ms_ssim_values else (None, None)
    return psnr_range, ms_ssim_range