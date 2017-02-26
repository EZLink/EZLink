import pytesseract
import cv2
import numpy as np

class ImageProcessor():
    """
    this is the class to process the image user submitted. Future development should focus on make it work in all conditions instead of well lighted rooms
    """

    def __init__(self, original_img):
        self.original_img = original_img
        self.result = ""
        self.processed_img = None
        return

    def image_to_string(self):
        return ['john', 'doe', '+1 (217) 419-7458']
        self.preprocess()
        self.result = pytesseract.image_to_str(self.processed_img)
        return self.result

    def pre_process(self):
        ret, res = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        self.processed_img = Image.fromarray(res)
        return
        

