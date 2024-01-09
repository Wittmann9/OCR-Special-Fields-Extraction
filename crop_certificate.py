# load the image
import cv2
def crop_certificate(path_to_certificate):
    image = cv2.imread(path_to_certificate)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(blurred, 10, 100)

    # define a (3, 3) structuring element
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # apply the dilation operation to the edged image
    dilate = cv2.dilate(edged, kernel, iterations=1)

    # find the contours in the dilated image
    contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    image_copy = image.copy()

    # Filter contours based on area and aspect ratio
    filtered_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)

        # Adjust these thresholds based on your image
        if area > 2000 and 0.5 < aspect_ratio < 4.5:
            filtered_contours.append(contour)

    # Iterate through the filtered contours
    for contour in filtered_contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Add additional filtering based on your criteria
        if w > 80 and h > 80:
            # Process the big rectangles as needed
            cv2.rectangle(image_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cropped_certificate = image[y:y + h, x:x + w]
            cv2.imwrite('cropped_certificate.jpg', cropped_certificate)
