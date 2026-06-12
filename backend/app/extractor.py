# import cv2
# import re
# import pytesseract

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# def read_text_from_roi(roi):
#     if roi is None or roi.size == 0:
#         return ""
    
#     gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#     text = pytesseract.image_to_string(gray)
#     return text.strip()


# def extract_structured_data(image_path):
#     img = cv2.imread(image_path)
#     h, w, _ = img.shape

#     data = {
#         "enrollment_no": None,
#         "co1": None,
#         "co2": None,
#         "co3": None,
#         "co4": None,
#         "co5": None,
#         "total": None
#     }

#     # =====================================================
#     # ENROLLMENT ROI
#     # =====================================================

#     enroll_roi = img[450:530, 730:1140]
#     enroll_text = read_text_from_roi(enroll_roi).upper()

#     print("\n===== ENROLL TEXT =====")
#     print(enroll_text)

#     clean_text = enroll_text.replace(" ", "").replace("\n", "")
#     match = re.search(r'0801[A-Z]{2}\d{4,6}', clean_text)
#     if match:
#         data["enrollment_no"] = match.group()

#     # =====================================================
#     # TOTAL COLUMN ROI
#     # =====================================================

#     total_roi = img[int(h*0.48):int(h*0.98), int(w*0.78):int(w*0.98)]
#     total_text = read_text_from_roi(total_roi)

#     print("\n===== TOTAL COLUMN TEXT =====")
#     print(total_text)

#     nums = re.findall(r'\d+', total_text)
#     nums = [int(n) for n in nums]
#     nums = [n for n in nums if n != 70]

#     print("FILTERED NUMBERS:", nums)

#     if len(nums) >= 2:
#         data["total"] = nums[0]
#         co_values = nums[1:]

#         if len(co_values) > 0: data["co1"] = co_values[0]
#         if len(co_values) > 1: data["co2"] = co_values[1]
#         if len(co_values) > 2: data["co3"] = co_values[2]
#         if len(co_values) > 3: data["co4"] = co_values[3]
#         if len(co_values) > 4: data["co5"] = co_values[4]

#     print("\n===== FINAL DATA =====")
#     print(data)

#     return data

from google.cloud import vision
import cv2
import re

client = vision.ImageAnnotatorClient()


# =====================================================
# OCR HELPER
# =====================================================

def read_text_from_roi(roi):

    if roi is None or roi.size == 0:
        return ""

    _, buffer = cv2.imencode(".jpg", roi)

    content = buffer.tobytes()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)

    texts = response.text_annotations

    if not texts:
        return ""

    return texts[0].description.strip()


# =====================================================
# MAIN EXTRACTOR
# =====================================================

def extract_structured_data(image_path):

    img = cv2.imread(image_path)

    h, w, _ = img.shape

    data = {
        "enrollment_no": None,
        "co1": None,
        "co2": None,
        "co3": None,
        "co4": None,
        "co5": None,
        "total": None
    }

    # =====================================================
    # ENROLLMENT ROI
    # =====================================================

    enroll_x1 = int(w * 0.52)
    enroll_x2 = int(w * 0.88)

    enroll_y1 = int(h * 0.18)
    enroll_y2 = int(h * 0.30)

    enroll_roi = img[enroll_y1:enroll_y2, enroll_x1:enroll_x2]

    cv2.imwrite("debug_enrollment.jpg", enroll_roi)

    enroll_text = read_text_from_roi(enroll_roi).upper()

    print("\n===== ENROLL TEXT =====")
    print(enroll_text)

    clean_text = (
        enroll_text
        .replace(" ", "")
        .replace("\n", "")
    )

    match = re.search(
        r'0801[A-Z]{2}\d{4,6}',
        clean_text
    )

    if match:
        data["enrollment_no"] = match.group()

    # =====================================================
    # TOTAL COLUMN ROI
    # =====================================================

    total_x1 = int(w * 0.78)
    total_x2 = int(w * 0.98)

    total_y1 = int(h * 0.48)
    total_y2 = int(h * 0.98)

    total_roi = img[
        total_y1:total_y2,
        total_x1:total_x2
    ]

    cv2.imwrite("debug_total_roi.jpg", total_roi)

    total_text = read_text_from_roi(total_roi)

    print("\n===== TOTAL COLUMN TEXT =====")
    print(total_text)

    nums = re.findall(r'\d+', total_text)

    nums = [int(n) for n in nums]

    print("RAW NUMBERS:", nums)

    # remove 70 ("OUT OF")
    nums = [n for n in nums if n != 70]

    print("FILTERED NUMBERS:", nums)

    # Expected:
    # [61,13,9,14,14,11]

    if len(nums) >= 2:

        grand_total = nums[0]

        co_values = nums[1:]

        data["total"] = grand_total

        if len(co_values) > 0:
            data["co1"] = co_values[0]

        if len(co_values) > 1:
            data["co2"] = co_values[1]

        if len(co_values) > 2:
            data["co3"] = co_values[2]

        if len(co_values) > 3:
            data["co4"] = co_values[3]

        if len(co_values) > 4:
            data["co5"] = co_values[4]

    # =====================================================
    # FINAL DEBUG
    # =====================================================

    print("\n===== FINAL DATA =====")
    print(data)

    return data