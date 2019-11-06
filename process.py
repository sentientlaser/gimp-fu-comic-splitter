## (D) Daniel Bertinshaw 2019
## This file is available under the LGPL 3.0 license: https://www.gnu.org/licenses/lgpl-3.0.txt
## 
## small script to process old 5.5" x 8" format comics where the 
## raw scans are 2-pages spreads.
## 
## loads all files, rotates them 270 degrees, applies some filters to 
## compensate for the yellowing caharacteristic of acid print pulp
## then crops left and right
## 
## Broken into smaller functions to allow easier parameter and process
## changes.
## 

from os import listdir, path
from gimpfu import *


def process_all_files(inpath, outpath):
 """ process all files found in `inpath` and place results in `outpath`
 """
 inpath = path.expanduser(inpath)

 def process_file(file, file_suffix, xoff): 
  """ process a single file
  """
  def load_image(file):
   """ Load a single file, return the gimp objects needed
   """
   image = pdb.file_png_load(inpath+file, file)
   drawable = pdb.gimp_image_active_drawable(image)
   display = pdb.gimp_display_new(image)
   return image, drawable, display

  def process_for_yellowing(image, drawable):
   """ applies filters to the image to compensate for the yellowing of acid printed pulp
   """
   gauss_radius = 1.5
   contrast_tweak = 100
   pdb.gimp_desaturate(drawable)
   pdb.gimp_brightness_contrast(drawable, 0, contrast_tweak)
   pdb.plug_in_gauss(image, drawable, gauss_radius, gauss_radius, 0)

  def process_crop_side(image, drawable, xoff):
   """ crops each side page from the scanned spread
   """
   width = 940
   height = 1400
   yoff = 170
   pdb.gimp_image_rotate(image, 2)
   pdb.gimp_image_crop(image, width, height, xoff, yoff)

  def save_and_dealloc(image, display, drawable, file, file_suffix):
   """ saves to outpath and deallocates the gimp objects
   """
   new_file = path.expanduser(outpath) + file.replace(".png", file_suffix + ".png")
   pdb.file_png_save(image, drawable, new_file, new_file, 1, 9, 1, 1, 1, 1, 1)
   pdb.gimp_display_delete(display)
   pdb.gimp_image_delete(image)
   print(new_file + " -> done")

  image, drawable, display = load_image(file)
  process_for_yellowing(image, drawable)
  process_crop_side(image, drawable, xoff)
  save_and_dealloc(image, display, drawable, file, file_suffix)

 files = listdir(inpath)
 for file in files:
  process_file(file, "1", 30)
  process_file(file, "2", 1110)

 print("all done")

# Start the process
process_all_files("~/Projects/Scans/Raw/", "~/Projects/Scans/Done/")





