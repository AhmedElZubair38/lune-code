import os
from PIL import Image
import pandas as pd

def has_transparency(img):
    """
    Checks if a PIL Image has a transparent background.
    """
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        if transparent != -1:
            return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True
    return False

def is_correct_size(img, target_size=(200, 200)):
    """
    Checks if the image has the exact target size (default 200x200).
    """
    return img.size == target_size

def analyze_image(file_path):
    """
    Runs all checks on an image and returns a dict with the results.
    """
    result = {
        'filename': os.path.basename(file_path),
        'has_transparency': None,
        'is_200x200': None,
        'is_valid': None,
        'error': None
    }

    try:
        with Image.open(file_path) as img:
            result['has_transparency'] = has_transparency(img)
            result['is_200x200'] = is_correct_size(img)
            result['is_valid'] = (
                not result['has_transparency'] and result['is_200x200']
            )
    except Exception as e:
        result['error'] = str(e)
        result['is_valid'] = False

    return result

def scan_image_folder(folder_path):
    """
    Scans a folder of images and returns a DataFrame with check results.
    """
    results = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.gif', '.tiff', '.webp')):
            file_path = os.path.join(folder_path, filename)
            results.append(analyze_image(file_path))
    
    return pd.DataFrame(results)

df = scan_image_folder("logo_transparent_test")
print(df)