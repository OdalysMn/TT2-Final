import cv2

class Player:

    def __init__(self, videoFile):
        self.capture = cv2.VideoCapture(videoFile)

    def getImagen(self):
        ret, img = self.capture.read()
        if(ret==True):
            return img
        else:
            return "error"

    def liberarCamara(self):
        self.capture.release()