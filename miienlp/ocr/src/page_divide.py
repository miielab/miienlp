{\rtf1\ansi\ansicpg1252\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww13140\viewh19980\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import cv2\
import numpy as np\
import os\
\
\
class PageDivide(object):\
    def __init__(self, file, output1, output2):\
        self.file = file\
        self.output = [output1, output2]\
        self.image = cv2.imread(self.file)\
        self.height, self.width, self.channel = self.image.shape\
\
\
    def divide_page(self):\
        '''\
        Split up scans with two pages on it into two images\
        '''\
        x = int(self.width/2)\
        w = int(self.width/2)\
        img1 = self.image[0:self.height, 0:w]\
        img2 = self.image[0:self.height, x:x+w]\
        cv2.imwrite(self.output[0], img1)\
        cv2.imwrite(self.output[1], img2)\
        return\
\
	}