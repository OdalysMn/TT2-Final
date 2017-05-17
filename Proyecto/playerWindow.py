import sys
from PyQt4 import uic, QtGui, QtCore
import cv2

class Player:

    def __init__(self, fileName):
        self.capture = cv2.VideoCapture(fileName)
        self.playFlag = True
        self.pauseFlag = False
        self.stopFlag = False

    def getImagen(self):
        ret, img = self.capture.read()
        if(ret==True):
            return img
        else:
            return "error"

class PlayerW:
    def __init__(self):
        # Cargamos la GUI desde el archivo UI.
        self.PlayerWindow = uic.loadUi('player.ui')

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    player = PlayerW()
    player.PlayerWindow.show()
    app.exec_()