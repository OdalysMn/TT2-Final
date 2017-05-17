#from SimpleCV import Image, Display
import os
import time

#img = Image('frames/frame0.jpg')
#hsv = img.toHSV()
#rgb = hsv.toRGB()


#while True:
    #hsv.show()
    #rgb.show()
path = 'C:/DirectorioCreadoConPython'

try:
    os.makedirs(path)
except OSError:
    if not os.path.isdir(path):
        raise