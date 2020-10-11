#!/usr/bin/env python3
from PIL import Image
import os

# To get the username from environment variable
USER = os.getenv("USER")
# Creating image directory path
image_directory = "/home/{}/supplier-data/images/".format(USER)
# listing all the files in the above directory.
files = os.listdir(image_directory)
# Looping through list of files.
for image_name in files:
    # Accepting files that has tiff extension and ignoring hidden files
    if not image_name.startswith(".") and "tiff" in image_name:
        # creating absolute path for each image
        image_path = image_directory + image_name
        # removing the .tiff extension
        path = os.path.splitext(image_path)[0]
        # opening the image
        img = Image.open(image_path)
        # Adding jpeg format to the image
        new_path = "{}.jpeg".format(path)
        # 1. Converting the file to RGB. The raw images from images subdirectory contains alpha transparency layers.
        # So, it is better to first convert RGBA 4-channel format to RGB 3-channel format before processing the
        # images. Use convert("RGB") method for converting RGBA to RGB image.
        # 2. Then resizing it.
        # 3. Saving it to the new path with JPEG format.
        img.convert("RGB").resize((600, 400)).save(new_path, "JPEG")
