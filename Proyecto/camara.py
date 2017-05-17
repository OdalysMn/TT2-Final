import cv2

class Camara:

    def __init__(self, index):
        self.capture = cv2.VideoCapture(index)

    def getImagen(self):
        ret, img = self.capture.read()
        if(ret==True):
            return img
        else:
            return "error"

    def liberarCamara(self):
        self.capture.release()




