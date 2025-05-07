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
        if filename.lower().endswith(('.png', '.gif', '.tiff', '.webp', '.jpeg', '.jpg', 'jiff')):
            file_path = os.path.join(folder_path, filename)
            results.append(analyze_image(file_path))
    return pd.DataFrame(results)

def generate_summary_statistics(df):
    total = len(df)
    stats = {
        "Total Logos Analyzed": total,
        "Transparent Logos": df['has_transparency'].sum(),
        "Correct Size (200x200)": df['is_200x200'].sum(),
        "Blurry Logos": df['is_blurry'].sum(),
        "Logos with Excessive Empty Space": df['has_excessive_empty_space'].sum(),
        "Low Saturation Logos": df['is_low_saturation'].sum(),
        "Valid Logos": df['is_valid'].sum(),
        "Invalid Logos": (~df['is_valid']).sum(),
        "Errored Files": df['error'].notnull().sum()
    }
    return pd.DataFrame(list(stats.items()), columns=['Metric', 'Count'])

df = scan_image_folder(r"/Users/ahmed/Desktop/brand_logos")
summary_df = generate_summary_statistics(df)

output_path = "admin-data_LOGO-CHECKER_analysis_report.xlsx"
with pd.ExcelWriter(output_path) as writer:
    df.to_excel(writer, sheet_name="Logo Analysis Results", index=False)
    summary_df.to_excel(writer, sheet_name="Summary Statistics", index=False)

print(df)
print("Total rows:", len(df))





















# import os
# from PIL import Image, ImageStat
# import pandas as pd
# import cv2
# import numpy as np
# import math

# def has_transparency(img):
#     if img.info.get("transparency", None) is not None:
#         return True
#     if img.mode == "P":
#         img = img.convert("RGBA")
#         extrema = img.getextrema()
#         if extrema[3][0] < 255:
#             return True
#     elif img.mode == "RGBA":
#         extrema = img.getextrema()
#         if extrema[3][0] < 255:
#             return True
#     return False

# def is_correct_size(img, target_size=(200, 200)):
#     return img.size == target_size

# def get_blurriness_score(img):
#     img_cv = cv2.cvtColor(np.array(img.convert('RGB')), cv2.COLOR_RGB2GRAY)
#     return cv2.Laplacian(img_cv, cv2.CV_64F).var()

# def has_excessive_empty_space(img, threshold_ratio=0.5):
#     img_cv = cv2.cvtColor(np.array(img.convert('RGB')), cv2.COLOR_RGB2GRAY)
#     _, thresh = cv2.threshold(img_cv, 240, 255, cv2.THRESH_BINARY_INV)
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     if not contours:
#         return True
#     x, y, w, h = cv2.boundingRect(np.vstack(contours))
#     logo_area = w * h
#     total_area = img.size[0] * img.size[1]
#     return (logo_area / total_area) < (1 - threshold_ratio)

# def is_low_saturation(img, threshold=30):
#     img_cv = cv2.cvtColor(np.array(img.convert('RGB')), cv2.COLOR_RGB2HSV)
#     mean_sat = np.mean(img_cv[:, :, 1])
#     return mean_sat < threshold

# def analyze_image(file_path):
#     result = {
#         'filename': os.path.basename(file_path),
#         'has_transparency': None,
#         'is_200x200': None,
#         'blurriness_score': None,
#         'is_blurry': None,
#         'has_excessive_empty_space': None,
#         'is_low_saturation': None,
#         'is_valid': None,
#         'error': None
#     }
#     try:
#         with Image.open(file_path) as img:
#             if img.mode == "P":
#                 img = img.convert("RGBA")

#             result['has_transparency'] = has_transparency(img)
#             result['is_200x200'] = is_correct_size(img)
#             blur_score = get_blurriness_score(img)
#             result['blurriness_score'] = blur_score
#             result['is_blurry'] = blur_score < 500
#             result['has_excessive_empty_space'] = has_excessive_empty_space(img)
#             result['is_low_saturation'] = is_low_saturation(img)

#             result['is_valid'] = (
#                 not result['has_transparency']
#                 and result['is_200x200']
#                 and not result['is_blurry']
#                 and not result['has_excessive_empty_space']
#                 and not result['is_low_saturation']
#             )
#     except Exception as e:
#         result['error'] = str(e)
#         result['is_valid'] = False

#     return result

# def generate_summary_statistics(df):
#     total = len(df)
#     stats = {
#         "Total Logos Analyzed": total,
#         "Transparent Logos": df['has_transparency'].sum(),
#         "Correct Size (200x200)": df['is_200x200'].sum(),
#         "Blurry Logos": df['is_blurry'].sum(),
#         "Logos with Excessive Empty Space": df['has_excessive_empty_space'].sum(),
#         "Low Saturation Logos": df['is_low_saturation'].sum(),
#         "Valid Logos": df['is_valid'].sum(),
#         "Invalid Logos": (~df['is_valid']).sum(),
#         "Errored Files": df['error'].notnull().sum()
#     }
#     return pd.DataFrame(list(stats.items()), columns=['Metric', 'Count'])

# def batch_and_process(folder_path, num_batches=8, output_prefix="LOGO-CHECKER-RESULTS/admin-data_LOGO-CHECKER_analysis_report"):
#     # 1. Gather all image files
#     extensions = ('.png', '.gif', '.tiff', '.webp', '.jpeg', '.jpg')
#     all_files = [os.path.join(folder_path, f)
#                  for f in os.listdir(folder_path)
#                  if f.lower().endswith(extensions)]
#     total = len(all_files)
#     batch_size = math.ceil(total / num_batches)

#     for i in range(num_batches):
#         start = i * batch_size
#         end = min(start + batch_size, total)
#         batch_files = all_files[start:end]

#         print(f"Processing batch {i+1}/{num_batches}: files {start+1}–{end}")

#         # Analyze batch
#         results = [analyze_image(fp) for fp in batch_files]
#         df_batch = pd.DataFrame(results)

#         # Summary stats
#         summary_df = generate_summary_statistics(df_batch)

#         # Write out to Excel
#         batch_label = f"{output_prefix} - BATCH {i+1}.xlsx"
#         with pd.ExcelWriter(batch_label) as writer:
#             df_batch.to_excel(writer, sheet_name="Logo Analysis Results", index=False)
#             summary_df.to_excel(writer, sheet_name="Summary Statistics", index=False)

#         print(f"  ➔ Written {batch_label}")

# if __name__ == "__main__":
#     folder = r"/Users/ahmed/Desktop/brand_logos"
#     batch_and_process(folder, num_batches=8)