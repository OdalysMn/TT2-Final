
import cv2
import numpy as np

def drawRectangleImage(name):
    image = cv2.imread(name)

    cv2.circle(image, (320, 240), 28, (0,255,0), -1)
    cv2.circle(image, (320, 240), 56, (0, 255, 0), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, '1', (320, 240), font, 1, (255, 255, 255), 1, 255)

    cv2.circle(image, (200,200), 28,(0,255,0), -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, '2', (200,200), font, 1, (255, 255, 255), 1, 255)

    cv2.circle(image, (590, 50), 28, (0,255,0), -1)
    cv2.circle(image, (590, 50), 56, (0, 255, 0), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, '3', (590, 50), font, 1, (255, 255, 255), 1, 255)

    cv2.circle(image, (590, 430), 28, (0,255,0), -1)
    cv2.circle(image, (590, 430), 56, (0, 255, 0), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, '4', (590, 430), font, 1, (255, 255, 255), 1, 255)

    cv2.circle(image, (320, 430), 28,(0,255,0), -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, '5', (320, 430), font, 1, (255, 255, 255), 1, 255)

    return image

def drawTriangle(name):
    image = cv2.imread(name)

    cv2.circle(image, (320, 50), 28, (0,255,0), -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, '1', (320, 50), font, 1, (255, 255, 255), 1, 255)

    cv2.circle(image, (590, 430), 28, (0,255,0), -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, '2', (590, 430), font, 1, (255, 255, 255), 1, 255)

    cv2.circle(image, (50, 430), 28, (0,255,0), -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, '3', (50, 430), font, 1, (255, 255, 255), 1, 255)

    return image

rectangle = drawRectangleImage('imagenPrueba.jpg')
#triangle = drawTriangle('imagenPrueba.jpg')

cv2.imwrite('imagenPruebaR.jpg', rectangle)
#cv2.imwrite('imagenPruebaT.jpg', triangle)

cv2.imshow('rectangle', rectangle)
#cv2.imshow('triangle', triangle)

cv2.waitKey()
cv2.destroyAllWindows()

