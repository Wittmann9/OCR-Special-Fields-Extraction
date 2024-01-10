import pickle
import cv2
import numpy as np
import os
import torch
import PIL
try:
  from PIL import Image
except ImportError:
  import  Image

os.makedirs('resized_images', exist_ok=True)

def set_image_dpi(image_path):
  im = Image.open(image_path)
  length_x, width_y = Image.open(image_path).size
  factor = min(1, float(1024.0 / length_x))
  size = int(factor * length_x), int(factor * width_y)
  im_resized = im.resize(size, PIL.Image.Resampling.LANCZOS)

  # temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=’.png’)
  # temp_filename = temp_file.name
  img = im_resized.save(f"resized_images/resized_{image_path}".replace("/", "-"), dpi=(300, 300))
  return im_resized

def sharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
  """Return a sharpened version of the image, using an unsharp mask."""
  blurred = cv2.GaussianBlur(image, kernel_size, sigma)
  sharpened = float(amount + 1) * image - float(amount) * blurred
  sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
  sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
  sharpened = sharpened.round().astype(np.uint8)
  if threshold > 0:
    low_contrast_mask = np.absolute(image - blurred) < threshold
    np.copyto(sharpened, image, where=low_contrast_mask)
  return sharpened

def distance_transform(img):
  # distance transform which calculates the distance to the
  # closest zero pixel for each pixel in the input image
  dist = cv2.distanceTransform(img, cv2.DIST_L2, 5)
  # normalize the distance transform such that the distances lie in
  # the range [0, 1] and then convert the distance transform back to
  # an unsigned 8-bit integer in the range [0, 255]
  dist = cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
  dist = (dist * 255).astype("uint8")
  # threshold the distance transform using Otsu's method
  dist = cv2.threshold(dist, 0, 255,
    cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
  return dist

def preprocess_image(path_to_img):
  #resize image
  resized = set_image_dpi(path_to_img)
  width, length = Image.open(path_to_img).size
  resized = cv2.imread(f"resized_images/resized_{path_to_img}".replace("/", "-"))

  #enlarge image
  up_points = (width*2, length*2)
  enlarged = cv2.resize(resized, up_points, interpolation= cv2.INTER_LINEAR)

  #sharpen image
  sharpened_image = sharp_mask(enlarged)

  # convert it to grayscale
  gray = cv2.cvtColor(sharpened_image, cv2.COLOR_BGR2GRAY)

  #Otsu threshold
  # thresh = cv2.threshold(gray, 0, 255,
  #   cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
  #
  # #distance_transform
  # dist = distance_transform(thresh)
  #
  # #erosion
  # kernel = np.ones((2,2),np.uint8)
  # erosion = cv2.erode(dist, kernel,iterations = 1)
  #
  # #rotate image
  # rotated = cv2.rotate(erosion, cv2.ROTATE_90_CLOCKWISE)
  return gray
  # return rotated







