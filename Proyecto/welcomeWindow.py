import sys
from PyQt4 import uic, QtGui, QtCore
from mainWindow import GUI
from analyzeWindow import Analyze
from playerWindow import PlayerW

class Welcome:
    def __init__(self):
        # Cargamos la GUI desde el archivo UI.
        self.WelcomeWindow = uic.loadUi('welcome.ui')
        self.WelcomeWindow.btnGrabarPrueba.clicked.connect(lambda:self.create_new_window(self.WelcomeWindow.btnGrabarPrueba))
        self.WelcomeWindow.btnAnalizarVideo.clicked.connect(lambda: self.create_new_window(self.WelcomeWindow.btnAnalizarVideo))
        self.WelcomeWindow.btnVerVideos.clicked.connect(lambda: self.create_new_window(self.WelcomeWindow.btnVerVideos))
        self.WelcomeWindow.btnSalir.clicked.connect(lambda: self.create_new_window(self.WelcomeWindow.btnSalir))

    def create_new_window(self,btn):

        if btn.text() == 'Grabar Prueba':
            self.newWindow = GUI()
            self.newWindow.MainWindow.show()
            self.WelcomeWindow.close()


        elif btn.text() == 'Analizar Video':
            self.newWindow = Analyze()
            self.newWindow.AnalyzeWindow.show()
            self.WelcomeWindow.close()

        elif btn.text() == 'Videos Analizados':
            self.newWindow = PlayerW()
            self.newWindow.PlayerWindow.show()
            self.WelcomeWindow.close()

        else:
            self.WelcomeWindow.close()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    gui = Welcome()
    gui.WelcomeWindow.show()
    app.exec_()
