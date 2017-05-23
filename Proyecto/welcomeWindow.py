import sys
from db import DB
from sistema import Sistema
from mainWindow import Main
from PyQt4 import uic, QtGui, QtCore

class Welcome:
    def __init__(self):
        # Cargamos la GUI desde el archivo UI.
        self.WelcomeWindow = uic.loadUi('welcome.ui')
        self.WelcomeWindow.btnGrabarPrueba.clicked.connect(lambda:self.create_new_window(self.WelcomeWindow.btnGrabarPrueba))
        self.WelcomeWindow.btnSalir.clicked.connect(lambda: self.create_new_window(self.WelcomeWindow.btnSalir))

        db = DB()
        lastVideo = db.getTheLastVideo()

        self.idVideo = lastVideo.idVideo + 1
        self.idPrueba = lastVideo.idPrueba + 1

        print "idVideo: ", self.idVideo
        print "idPrueba: ", self.idPrueba

        sistema = Sistema()
        sistema.createDirectory('EyeTracking/Prueba' + str(self.idPrueba))
        sistema.createDirectory('EyeTracking/Prueba' + str(self.idPrueba) + '/Videos')
        sistema.createDirectory('EyeTracking/Prueba' + str(self.idPrueba) + '/Frames')
        sistema.createDirectory('EyeTracking/Prueba' + str(self.idPrueba) + '/Frames/FramesOjo')
        sistema.createDirectory('EyeTracking/Prueba' + str(self.idPrueba) + '/Frames/FramesEscena')
        sistema.createDirectory('EyeTracking/Prueba' + str(self.idPrueba) + '/Frames/FramesPupila')
        sistema.createDirectory('EyeTracking/Prueba' + str(self.idPrueba) + '/Frames/FramesTray')

    def create_new_window(self,btn):

        if btn.text() == 'Grabar Prueba':
            self.newWindow = Main(self.idVideo,self.idPrueba)
            self.newWindow.MainWindow.show()
            self.WelcomeWindow.close()

        else:
            self.WelcomeWindow.close()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    gui = Welcome()
    gui.WelcomeWindow.show()
    app.exec_()
