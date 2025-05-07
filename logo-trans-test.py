import os
from PIL import Image
import pandas as pd

def has_transparency(img):
    """
    Checks if a given PIL Image has a transparent background.
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

def scan_logos_for_transparency(folder_path):
    """
    Reads all images in a folder and returns a DataFrame showing whether each has a transparent background.
    """
    results = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.gif', '.tiff', '.webp')):
            file_path = os.path.join(folder_path, filename)
            try:
                with Image.open(file_path) as img:
                    transparent = has_transparency(img)
                    results.append({'filename': filename, 'has_transparency': transparent})
            except Exception as e:
                results.append({'filename': filename, 'has_transparency': None, 'error': str(e)})
    
    return pd.DataFrame(results)

# Example usage:
df = scan_logos_for_transparency("logo_transparent_test")
print(df)

