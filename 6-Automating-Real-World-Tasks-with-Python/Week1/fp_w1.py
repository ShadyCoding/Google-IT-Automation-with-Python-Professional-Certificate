#!/usr/bin/env python3
import os, sys
from PIL import Image
old_images = os.path.expanduser('~') + '/images/'
updated_images = '/opt/icons/'
for image in os.listdir(old_images):
    try:
        if  '.' not in image[0]:
            img = Image.open(old_images + image)
            img.rotate(-90).resize((128, 128)).convert("RGB").save(updated_images + image + '.jpeg')
            img.close()
    except OSError:
        print("OSError")
