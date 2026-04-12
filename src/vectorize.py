from PIL import Image
import matplotlib.image as mpimg
import numpy as np
import os
import shutil

# =========================
# FIXED PATH SETUP
# =========================
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

randomdata_root = os.path.join(project_root, 'randomdata')
vectorize_root = os.path.join(project_root, 'vectorize_data')

# wipe old vectorized data safely
shutil.rmtree(vectorize_root, ignore_errors=True)

# =========================
# IMAGE CONVERTER FUNCTION
# =========================
def get_images(classification):
    plants_dir = os.path.join(randomdata_root, classification)
    plants_vectorize_dir = os.path.join(vectorize_root, classification)

    os.makedirs(plants_vectorize_dir, exist_ok=True)

    if not os.path.isdir(plants_dir):
        print(f"Error: Directory not found at {plants_dir}")
        return

    for filename in os.listdir(plants_dir):
        try:
            if filename.lower().endswith('.jpg'):

                image_full_path = os.path.join(plants_dir, filename)

                image = mpimg.imread(image_full_path)
                img_array = np.array(image)

                base_filename = os.path.splitext(filename)[0]
                output_full_path = os.path.join(plants_vectorize_dir, base_filename + ".npy")

                # skip if already exists
                if os.path.exists(output_full_path):
                    continue

                np.save(output_full_path, img_array)

        except Exception as e:
            print(f"ERROR on file: {filename}")
            print(e)


# =========================
# RUN ALL CLASSES
# =========================
classes = ["bac", "fung", "hea", "pes", "vir"]

for c in classes:
    get_images(c)