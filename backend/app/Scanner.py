import cv2
import numpy as np
from imutils.perspective import four_point_transform


def scan_document(image_path):

    image = cv2.imread(image_path)

    ratio = image.shape[0] / 500.0

    orig = image.copy()

    # ==========================================
    # Resize
    # ==========================================

    resized = cv2.resize(image, (700, 500))

    # ==========================================
    # Preprocess
    # ==========================================

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    edged = cv2.Canny(blur, 75, 200)

    # ==========================================
    # Find contours
    # ==========================================

    contours, _ = cv2.findContours(
        edged.copy(),
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contours = sorted(
        contours,
        key=cv2.contourArea,
        reverse=True
    )[:5]

    screen_contour = None

    # ==========================================
    # Detect document contour
    # ==========================================

    for c in contours:

        peri = cv2.arcLength(c, True)

        approx = cv2.approxPolyDP(
            c,
            0.02 * peri,
            True
        )

        if len(approx) == 4:
            screen_contour = approx
            break

    # ==========================================
    # If contour not found
    # ==========================================

    if screen_contour is None:

        print("Document contour not found")

        return image_path

    # ==========================================
    # Perspective transform
    # ==========================================

    warped = four_point_transform(
        orig,
        screen_contour.reshape(4, 2) * ratio
    )

    # ==========================================
    # Save aligned image
    # ==========================================

    output_path = "scanned_output.jpg"

    cv2.imwrite(output_path, warped)

    print("Scanned image saved")

    return output_path