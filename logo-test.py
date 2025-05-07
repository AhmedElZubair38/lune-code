import os
import cv2

folder_path = 'logo_test_folder'
min_resolution = (150, 150)
blur_threshold = 100.0

def is_clear(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return lap_var > blur_threshold, lap_var

for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        file_path = os.path.join(folder_path, filename)
        image = cv2.imread(file_path)
        if image is None:
            print(f"[SKIPPED] {filename}: Not a readable image.")
            continue

        h, w = image.shape[:2]
        resolution_ok = w >= min_resolution[0] and h >= min_resolution[1]
        clear, laplacian_var = is_clear(image)

        status = []
        if resolution_ok:
            status.append("✔ Resolution OK")
        else:
            status.append("❌ Low Resolution")

        if clear:
            status.append("✔ Clear")
        else:
            status.append(f"❌ Blurry (Var: {laplacian_var:.2f})")

        print(f"{filename}: {' | '.join(status)}")