#from SimpleCV import Image, Display
import os
import time

#img = Image('frames/frame0.jpg')
#hsv = img.toHSV()
#rgb = hsv.toRGB()


#while True:
    #hsv.show()
    #rgb.show()
"""path = 'C:/DirectorioCreadoConPython'

try:
    os.makedirs(path)
except OSError:
    if not os.path.isdir(path):
        raise"""
import cv2
import numpy as np

count = 0
fourcc = cv2.cv.CV_FOURCC('i', 'Y', 'U', 'V')
out = cv2.VideoWriter('output4.avi', fourcc, 20.0, (640,480))

while count < 121:
    pupilImage = cv2.imread('imagenPruebaR.jpg')
    cv2.imwrite("frames4/%d.jpg" % count, pupilImage)
    out.write(pupilImage)

    count = count +1