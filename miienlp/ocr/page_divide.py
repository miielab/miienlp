import cv2
import numpy as np
import os


class PageDivide(object):
    def __init__(self, file, output1, output2):
        self.file = file
        self.output = [output1, output2]
        self.image = cv2.imread(self.file)
        self.height, self.width, self.channel = self.image.shape


    def divide_page(self):
        '''
        Split up scans with two pages on it into two images
        '''
        x = int(self.width/2)
        w = int(self.width/2)
        img1 = self.image[0:self.height, 0:w]
        img2 = self.image[0:self.height, x:x+w]
        cv2.imwrite(self.output[0], img1)
        cv2.imwrite(self.output[1], img2)
        return

