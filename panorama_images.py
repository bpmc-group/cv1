# Copied from OpenCV Free Tutorials Lesson 9
# NOTE: it doesn't work like it does on Colab version in Jupyter

# Import Libraries
import os
import cv2
import math
import glob
import numpy as np
import matplotlib.pyplot as plt

from zipfile import ZipFile
from urllib.request import urlretrieve

#%matplotlib inline

#Download images
def download_and_unzip(url, save_path):
    print(f"Downloading and extracting assests....", end="")

    # Downloading zip file using urllib package.
    urlretrieve(url, save_path)

    try:
        # Extracting zip file using the zipfile package.
        with ZipFile(save_path) as z:
            # Extract ZIP file contents in the same directory.
            z.extractall(os.path.split(save_path)[0])

        print("Done")

    except Exception as e:
        print("\nInvalid file.", e)

URL = r"https://www.dropbox.com/s/0o5yqql1ynx31bi/opencv_bootcamp_assets_NB9.zip?dl=1"

asset_zip_path = os.path.join(os.getcwd(), "opencv_bootcamp_assets_NB9.zip")

# Download if asset ZIP does not exists.
if not os.path.exists(asset_zip_path):
    download_and_unzip(URL, asset_zip_path)

#Steps for Creating Panoramas
#    Find keypoints in all images
#    Find pairwise correspondences
#    Estimate pairwise Homographies
#    Refine Homographies
#    Stitch with Blending

# Read Images
imagefiles = glob.glob(f"boat{os.sep}*")
imagefiles.sort()

images = []
for filename in imagefiles:
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    images.append(img)

num_images = len(images)

# Display Images - this doesn't work - nothing shows 
plt.figure(figsize=[30, 10])
num_cols = 3
num_rows = math.ceil(num_images / num_cols)
for i in range(0, num_images):
    plt.subplot(num_rows, num_cols, i + 1)
    plt.axis("off")
    plt.imshow(images[i])

# Use the stitcher class
# Stitch Images
stitcher = cv2.Stitcher_create()
status, result = stitcher.stitch(images)

# added this to write and save the image
cv2.imwrite("pano_image.jpg", result)

if status == 0:
    plt.figure(figsize=[30, 10])
    plt.imshow(result)