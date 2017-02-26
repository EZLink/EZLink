import pytesseract
import cv2
import numpy as np
import re
from PIL import Image

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
        self.preprocess()
        self.result = pytesseract.image_to_string(self.processed_img)
        return self.result

    def preprocess(self):
        ret, res = cv2.threshold(self.original_img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        self.processed_img = Image.fromarray(res)
        return
        

class TextExtract():
    """
    this is the class to regex parse all the info we need from the string
    """

    def __init__(self, raw_string):
        self.raw_string = raw_string
        print(raw_string)
    
    def extract(self):
        self.first, self.last = self.extract_name()
        self.number = self.extract_number()
        return [self.first, self.last, self.number]

    def extract_name(self):
        all_matches = re.findall('[A-Z][a-z,A-Z]+', self.raw_string)
        if len(all_matches)>=1:
            return all_matches[0], all_matches[1]
        else:
            return "can't", "tell"


    def extract_number(self):
        all_matches = re.findall('\d{3}\D\d{3}\D\d{4}', self.raw_string)
        if all_matches:
            return all_matches[0]
        else:
            return ''

