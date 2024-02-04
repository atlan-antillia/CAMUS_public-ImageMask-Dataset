"""
This CAMUSImageMaskDataset.sitk_load method has been taken from the following code.

CAMUS_public/jupyter/script_camus_ef.ipynb

Citation
You have to refer to this citation for any use of the CAMUS database

S. Leclerc, E. Smistad, J. Pedrosa, A. Ostvik, et al.
"Deep Learning for Segmentation using an Open Large-Scale Dataset in 2D Echocardiography" in IEEE Transactions on Medical Imaging, vol. 38, no. 9, pp. 2198-2210, Sept. 2019
doi: 10.1109/TMI.2019.2900516

"""
from ctypes import resize
import os
import logging
from sys import float_repr_style
import cv2
import shutil
import glob

from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
from PIL import Image, ImageOps
import SimpleITK as sitk
from PIL.Image import Resampling
from skimage.measure import find_contours
import traceback

logger = logging.getLogger(__name__)

class CAMUSImageMaskDatasetGenerator:
  def __init__(self, resize=512):
    self.IMAGE_FILEPATTERN = "*.nii.gz"
    self.MASK_FILEPATTERN  = "*_gt.nii.gz"
    self.RESIZE            = resize

  def generate(self, input_dir, output_dir):
    mask_files = glob.glob(input_dir + "/*/*_gt.nii.gz")
    images_output_dir = os.path.join(output_dir, "images")
    masks_output_dir = os.path.join(output_dir, "masks")

    if  os.path.exists(images_output_dir):
      shutil.rmtree(images_output_dir)
    if  not os.path.exists(images_output_dir):
      os.makedirs(images_output_dir)

    if  os.path.exists(masks_output_dir):
      shutil.rmtree(masks_output_dir)
    if  not os.path.exists(masks_output_dir):
      os.makedirs(masks_output_dir)

    for mask_file in mask_files:
      image_file = mask_file.replace("_gt", "")
      self.generate_one(mask_file,  masks_output_dir, mask=True)  
      self.generate_one(image_file, images_output_dir, mask=False)      


  def generate_one(self, filepath, output_dir, mask=False):
    xndarray, info = self.sitk_load(filepath)
    shape = xndarray.shape
    print("--- shape {}",format(shape))
    if len(shape) == 2:  
      h = shape[0]
      w = shape[1]
      print(" --w {} h {}".format(w, h))
      basename = os.path.basename(filepath)
      name     = basename.split(".")[0]
      output_filepath = os.path.join(output_dir, name + ".jpg")
      if mask:
        xndarray = xndarray * 255.0
        xndarray = xndarray.astype('uint8')
        output_filepath = output_filepath.replace("_gt", "")
        
      #cv2.imwrite(output_filepath, xndarray)
      image = self.resize_to_square(xndarray, RESIZE= self.RESIZE)
      image.save(output_filepath, "JPEG", quality=95)
      print("Saved {}".format(output_filepath))

      # Create mirrored image
      filename = os.path.basename(output_filepath)
      mirrored = ImageOps.mirror(image)
      output_filename = "mirrored_" + filename
      image_filepath = os.path.join(output_dir, output_filename)
    
      mirrored.save(image_filepath, "JPEG", quality=95)
      print("=== Saved {}".format(image_filepath))
        

  def resize_to_square(self, image, RESIZE=512):
     image = Image.fromarray(image)
     w, h = image.size
     bigger = w
     if h >bigger:
       bigger = h
     background = Image.new("RGB", (bigger, bigger))
     x = (bigger - w)//2
     y = (bigger - h)//2

     background.paste(image, (x, y))
     background = background.resize((RESIZE, RESIZE))
     return background

  def sitk_load(self, filepath: str | Path) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Loads an image using SimpleITK and returns the image and its metadata.

    Args:
        filepath: Path to the image.

    Returns:
        - ([N], H, W), Image array.
        - Collection of metadata.
    """
    # Load image and save info
    image = sitk.ReadImage(str(filepath))
    info = {"origin": image.GetOrigin(), "spacing": image.GetSpacing(), "direction": image.GetDirection()}

    # Extract numpy array from the SimpleITK image object
    im_array = np.squeeze(sitk.GetArrayFromImage(image))

    return im_array, info

if __name__ == "__main__":
  try:
     input_dir = "./CAMUS_public/database_nifti"
     output_dir = "./CAMUS-master"
     if os.path.exists(output_dir):
       shutil.rmtree(output_dir)

     if not os.path.exists(output_dir):
       os.makedirs(output_dir)

     generator = CAMUSImageMaskDatasetGenerator()
     generator.generate(input_dir, output_dir)

  except:
    traceback.print_exc()
