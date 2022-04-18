import sys, os
import numpy as np
from PIL import Image as im
from scipy.ndimage import interpolation as inter
import cv2
from shutil import copyfile

# Right now, this script only compresses images if they need to be compresed

class Preprocess(object):
    def __init__(self, scan, output):
        self.file = scan
        self.output = output
        self.image = cv2.imread(self.file)

    def run_preprocessing(self):
        '''
        If preprocessed image already exists, return. Otherwise, compress image.
        '''
        if os.path.exists(self.output):
            return
        self.compress()

    def compress(self):
        '''
        Make image a jpg, and if it is greater than 10MB, then compress it.
        '''
        if self.image is not None:
            if os.path.getsize(self.file) < 10*1024*1024:
                print("Image size is less than 10 MB")
                compression_params = [cv2.IMWRITE_JPEG_QUALITY, 100]
                copyfile(self.file, self.output)
            else:
                # Compress image
                compression_params = [cv2.IMWRITE_JPEG_QUALITY, 100]
                cv2.imwrite(self.output, self.image)
                index = 1
                while os.path.getsize(self.output)/(1024*1024) >= 10:
                    compression_params = [cv2.IMWRITE_JPEG_QUALITY, 100-index]
                    cv2.imwrite(self.output, self.image, compression_params)
                    index += 1
                print("Image compressed to 10 MB threshold")
        else:
            print("Image cannot be read: " + self.file)


    def skew(self):
    	data = inter.rotate(bin_img, best_angle, reshape=False, order=0)
    	img = im.fromarray((255 * data).astype("uint8")).convert("RGB")

    def find_score(self, arr, angle):
    	data = inter.rotate(arr, angle, reshape=False, order=0)
    	hist = np.sum(data, axis=1)
    	score = np.sum((hist[1:] - hist[:-1]) ** 2)
    	return hist, score
    
    # get grayscale image
    def get_grayscale(self):
        self.image = cv2.imread(self.output)
        cv2.imwrite(self.output, cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY))

    # noise removal
    def remove_noise(self):
        self.image = cv2.imread(self.output)
        cv2.imwrite(self.output, cv2.medianBlur(self.image,5))
     
    #thresholding
    def thresholding(self):
        return cv2.threshold(self.image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    #dilation
    def dilate(self):
        kernel = np.ones((5,5),np.uint8)
        return cv2.dilate(self.image, kernel, iterations = 1)
        
    #erosion
    def erode(self):
        kernel = np.ones((5,5),np.uint8)
        return cv2.erode(self.image, kernel, iterations = 1)

    #opening - erosion followed by dilation
    def opening(self):
        kernel = np.ones((5,5),np.uint8)
        return cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel)

    #canny edge detection
    def canny(self):
        return cv2.Canny(self.image, 100, 200)

    #skew correction
    def deskew(self):
        self.image = cv2.imread(self.output)
        coords = np.column_stack(np.where(self.image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = self.image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(self.image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        cv2.imwrite(self.output, rotated)

    #template matching
    def match_template(self, template):
        return cv2.matchTemplate(self.image, template, cv2.TM_CCOEFF_NORMED) 


