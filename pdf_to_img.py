from pdf2image import convert_from_path
try:
  from PIL import Image
except ImportError:
  import Image

def pdf_to_img(pdf_name, poppler_path):
  image = convert_from_path(f"{pdf_name}.pdf", 350, poppler_path=poppler_path)
  image[0].save(f"{pdf_name}.jpg", "JPEG")
  return f"{pdf_name}.jpg"


