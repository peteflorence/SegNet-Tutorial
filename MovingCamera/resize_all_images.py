# This script reads all of the files in ./train
# and resizes all .png files to be 480 x 360
#
###  Input:  .png files in ./train
###  Output: .png files resized to 480 x 360

import os
import re
from PIL import Image

def resizeImage(filename):
  im_in = Image.open(filename)
  # adjust width and height to your needs
  width = 480
  height = 360
  # use one of these filter options to resize the image
  print filename
  im_out = im_in.resize((width, height), Image.ANTIALIAS)    # best down-sizing filter
  im_out.save(filename)


png_pattern = re.compile(".png")

cwd = os.getcwd()

path_to_train = cwd + "/train"
for root, dirs, files in os.walk(path_to_train):
    for filename in sorted(files):
        filename_full_path = os.path.join(root, filename)
        if png_pattern.search(filename_full_path) is not None:
            print "found .png match: " + filename_full_path
            resizeImage(filename_full_path)
