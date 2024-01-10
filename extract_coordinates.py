import cv2
import numpy as np
import pickle



def extract_coordinates(img_path, path_to_certificate):
    # resize image with contours
    contour = cv2.imread(img_path)
    certificate = cv2.imread(path_to_certificate)

    cert_rotated = cv2.rotate(certificate, cv2.ROTATE_90_CLOCKWISE)

    image = cv2.resize(contour, (cert_rotated.shape[1], cert_rotated.shape[0]))

    #extract contours
    # image = cv2.imread(img_path)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the blue color in HSV
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Create a mask for the blue color
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Remove dotted lines
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 500:
            cv2.drawContours(mask, [c], -1, (0, 0, 0), -1)

    # Fill contours
    close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    close = 255 - cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_kernel, iterations=4)
    cnts = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    contour_coordinates = []  # List to store contour coordinates

    for c in cnts:
        area = cv2.contourArea(c)
        if area < 5000:
            cv2.drawContours(close, [c], -1, (0, 0, 0), -1)
            # x, y, w, h = cv2.boundingRect(c)
            # contour_coordinates.append((x, y, x + w, y + h))  # Save contour coordinates

    # Smooth contours
    close = 255 - close
    open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(close, cv2.MORPH_OPEN, open_kernel, iterations=2)

    # Busca los contornos y dibuja los resultados
    ROI_number = 0
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        cv2.drawContours(image, [c], -1, (36, 255, 36), 3)
        x, y, w, h = cv2.boundingRect(c)
        ROI = image[y:y + h, x:x + w]
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        ROI_number += 1

        x, y, w, h = cv2.boundingRect(c)
        contour_coordinates.append((x, y, x + w, y + h))


    #save the coordinates
    pickle_coordinates = "coordinates"
    print(contour_coordinates)
    with open(pickle_coordinates, "wb") as fp:   #Pickling
      pickle.dump(contour_coordinates, fp)

    return pickle_coordinates


