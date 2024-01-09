import argparse
from pdf_to_img import pdf_to_img
from image_preprocessing import preprocess_image
from extract_coordinates import extract_coordinates
import easyocr
from easyocr import Reader
from crop_certificate import crop_certificate
import pickle
import cv2
import os
import torch


os.mkdir('temp')
def read_text(image_name, reader_name, in_line=True):

  # Read the data
  text = reader_name.readtext(image_name, detail = 0, paragraph=in_line)

  # Join texts writing each text in new line
  return '\n'.join(text)

if __name__ == '__main__':
    # pdf_to_image
    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf_name', type=str, default="Inspection_Certificate")
    parser.add_argument('--poppler_path', type=str, default="venv//Lib//site-packages//poppler-23.11.0//Library//bin")
    parser.add_argument('--gpu_availability', type=bool, default=True)
    args = parser.parse_args()


    reader_en_ch = easyocr.Reader(['en', 'ch_sim'], gpu=args.gpu_availability)

    path_to_certificate_img = pdf_to_img(args.pdf_name, args.poppler_path)
    crop_certificate(path_to_certificate_img)
    pickled_coordinates = extract_coordinates("cropped_countors.jpg", 'cropped_certificate.jpg')

    with open(pickled_coordinates, "rb") as fp:  # Unpickling
        coords = pickle.load(fp)
    print(coords)
    image = cv2.imread("cropped_certificate.jpg")
    rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    # cv2.imshow("rotated", image)
    # cv2.waitKey(0)  # wait for a keyboard input
    # cv2.destroyAllWindows()
    ocred_text = []
    for i, coord in enumerate(coords):
        print(i, coord)
        x1, y1, x2, y2 = coord
        cropped_roi = rotated[y1:y2, x1:x2]
        # cropped_roi.save(f"img_{i}.jpg")
        cv2.imwrite(os.path.join('temp', f"image_{i}.jpg"), cropped_roi)
        # cv2.imshow(f"image_{i}.jpg", cropped_roi)
        # cv2.waitKey(0)   #wait for a keyboard input
        # cv2.destroyAllWindows()
        preproc_image = preprocess_image(os.path.join('temp', f"image_{i}.jpg"))
        text = read_text(preproc_image, reader_en_ch)
        if not text == '':
            ocred_text.append(text)
        # print(text)
    print(ocred_text)

