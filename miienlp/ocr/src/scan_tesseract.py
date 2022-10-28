import cv2
import os, sys
import pytesseract
import numpy as np
pytesseract.pytesseract.tesseract_cmd = "C:\Program Files (x86)\Tesseract-OCR\\tesseract.exe" 


class ScanTesseract(object):
    def __init__(self, scan, output):
        self.file = scan
        self.output = output

    def run_tess(self):
    	# do not run if file already exists
    	if os.path.exists(self.output):
    		return
    	img = cv2.imread(self.file)
    	text = pytesseract.image_to_string(img)
    	print(text)