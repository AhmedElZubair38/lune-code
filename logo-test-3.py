import os
from PIL import Image, ImageStat
import pandas as pd
import cv2
import numpy as np

def has_transparency(img):

    if img.info.get("transparency", None) is not None:
        return True

    if img.mode == "P":
        img = img.convert("RGBA")
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False

def is_correct_size(img, target_size=(200, 200)):
    return img.size == target_size

def get_blurriness_score(img):
    img_cv = cv2.cvtColor(np.array(img.convert('RGB')), cv2.COLOR_RGB2GRAY)
    variance = cv2.Laplacian(img_cv, cv2.CV_64F).var()
    return variance

def is_blurry(img, threshold=500):
    return get_blurriness_score(img) < threshold

def has_excessive_empty_space(img, threshold_ratio=0.5):
    img_cv = cv2.cvtColor(np.array(img.convert('RGB')), cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(img_cv, 240, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return True

    x, y, w, h = cv2.boundingRect(np.vstack(contours))
    logo_area = w * h
    total_area = img.size[0] * img.size[1]
    return (logo_area / total_area) < (1 - threshold_ratio)

def is_low_saturation(img, threshold=30):
    img_cv = cv2.cvtColor(np.array(img.convert('RGB')), cv2.COLOR_RGB2HSV)
    saturation = img_cv[:, :, 1]
    mean_sat = np.mean(saturation)
    return mean_sat < threshold

def analyze_image(file_path):
    result = {
        'filename': os.path.basename(file_path),
        'has_transparency': None,
        'is_200x200': None,
        'is_blurry': None,
        'blurriness_score': None,
        'has_excessive_empty_space': None,
        'is_low_saturation': None,
        'is_valid': None,
        'error': None
    }

    try:
        with Image.open(file_path) as img:

            if img.mode == "P":
                img = img.convert("RGBA")

            result['has_transparency'] = has_transparency(img)
            result['is_200x200'] = is_correct_size(img)

            blur_score = get_blurriness_score(img)
            result['blurriness_score'] = blur_score
            result['is_blurry'] = blur_score < 500

            result['has_excessive_empty_space'] = has_excessive_empty_space(img)
            result['is_low_saturation'] = is_low_saturation(img)

            result['is_valid'] = (
                not result['has_transparency']
                and result['is_200x200']
                and not result['is_blurry']
                and not result['has_excessive_empty_space']
                and not result['is_low_saturation']
            )
    except Exception as e:
        result['error'] = str(e)
        result['is_valid'] = False

    return result

def scan_image_folder(folder_path):

    results = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.gif', '.tiff', '.webp', '.jpeg', '.jpg')):
            file_path = os.path.join(folder_path, filename)
            results.append(analyze_image(file_path))
    
    return pd.DataFrame(results)

df = scan_image_folder("logo_test_folder")
df.to_csv("logo_analysis_output.csv", index=False)
print(df)

print("Total rows:", len(df))