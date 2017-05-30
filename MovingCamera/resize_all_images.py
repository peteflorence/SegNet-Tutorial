# This script reads all of the files in ./train
# and resizes all .png files to be 480 x 360
#
###  Input:  .png files in ./train
###  Output: .png files resized to 480 x 360

import os
from PIL import Image

def resizeImage(filename):
  # adjust width and height to your needs
  width = 480
  height = 360
  # use one of these filter options to resize the image
  print filename
  try:
      im_in = Image.open(filename)
      if (im_in.size[0] == 480 and im_in.size[1] == 360):
          print "already 480 x 360"
          return
      im_out = im_in.resize((width, height), Image.ANTIALIAS)    # best down-sizing filter
      im_out.save(filename)
      print im_in.size, " --> ", im_out.size
  except(KeyboardInterrupt):
      quit()
  except:
      print "FAILED resizing"
      os.system("mv " + filename + " " + filename + "failed_resize")

def resizeDirectory(dir_name):
  cwd = os.getcwd()
  path_to_dir = cwd + "/" + dir_name
  for root, dirs, files in os.walk(path_to_dir):
      for filename in sorted(files):
          filename_full_path = os.path.join(root, filename)
          if filename_full_path.endswith(".png") and not filename_full_path.endswith("color_labels.png"):
              print "found .png match: " + filename_full_path
              resizeImage(filename_full_path)

resizeDirectory("train")
resizeDirectory("test")