import pytesseract
import cv2
import numpy as np
from PIL import Image

def extract_multipliers_from_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    lines = text.split("\n")
    multipliers = []
    for line in lines:
        if "x" in line:
            for part in line.split():
                if "x" in part:
                    try:
                        multipliers.append(part.strip().replace("x", ""))
                    except:
                        continue
    return multipliers[-10:]
