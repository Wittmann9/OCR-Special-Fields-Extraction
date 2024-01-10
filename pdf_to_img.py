from pdf2image import convert_from_path
try:
  from PIL import Image
except ImportError:
  import Image

def pdf_to_img(pdf_name):
  image = convert_from_path(f"{pdf_name}.pdf", 350)
  image[0].save(f"{pdf_name}.jpg", "JPEG")
  return f"{pdf_name}.jpg"





