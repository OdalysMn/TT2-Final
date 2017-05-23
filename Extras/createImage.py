
import cv2
import numpy as np

def drawRectangleImage(name):
    image = cv2.imread(name)
    cv2.circle(image, (50,50), 28, 255, -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, '1', (50,50), font, 1, (255, 255, 255), 1, 255)

    cv2.circle(image, (590, 50), 28, 255, -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, '2', (590, 50), font, 1, (255, 255, 255), 1, 255)

    cv2.circle(image, (590, 430), 28, 255, -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, '3', (590, 430), font, 1, (255, 255, 255), 1, 255)

    cv2.circle(image, (50, 430), 28, 255, -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, '4', (50, 430), font, 1, (255, 255, 255), 1, 255)

    return image

def drawTriangle(name):
    image = cv2.imread(name)

    cv2.circle(image, (320, 50), 28, 255, -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, '1', (320, 50), font, 1, (255, 255, 255), 1, 255)

    cv2.circle(image, (590, 430), 28, 255, -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, '2', (590, 430), font, 1, (255, 255, 255), 1, 255)

    cv2.circle(image, (50, 430), 28, 255, -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, '3', (50, 430), font, 1, (255, 255, 255), 1, 255)

    return image

rectangle = drawRectangleImage('imagenPrueba.jpg')
triangle = drawTriangle('imagenPrueba.jpg')

cv2.imwrite('imagenPruebaR.jpg', rectangle)
cv2.imwrite('imagenPruebaT.jpg', triangle)

cv2.imshow('rectangle', rectangle)
cv2.imshow('triangle', triangle)

cv2.waitKey()
cv2.destroyAllWindows()

