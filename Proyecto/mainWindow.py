import sys
import cv2
from PyQt4 import uic, QtGui, QtCore
from camara import Camara
from procesamiento import Procesamiento
from db import BD

class Main:
    def __init__(self):
        # Cargamos la GUI desde el archivo UI.
        self.MainWindow = uic.loadUi('main.ui')

        self.capturing = False
        self.seg = 0
        self.min = 0
        self.hrs = 0
        self.completed = 0
        self.center_points = []

        self.MainWindow.lblhrs.setText("00")
        self.MainWindow.lblmin.setText("00")
        self.MainWindow.lblseg.setText("00")

        self.camaraOjo = Camara(0)
        self.camaraEscena = Camara(2)
        """self.grabacionOjo = Grabacion(self.camaraOjo,'ojo1.avi',20.0,640,480)
        self.grabacionEscena = Grabacion(self.camaraEscena,'escena1.avi',20.0,640,480)"""

        self.MainWindow.btnAtras.clicked.connect(self.volver)
        self.MainWindow.btnGrabar.clicked.connect(self.iniciarGrabacion)
        self.MainWindow.btnGuardar.clicked.connect(self.terminarGrabacion)
        self.MainWindow.btnAnalizar.clicked.connect(self.analizarVideo)
        self.MainWindow.progBar.setValue(0)

        self.timer = QtCore.QTimer(self.MainWindow)
        self.MainWindow.connect(self.timer, QtCore.SIGNAL('timeout()'), self.show_frame)
        self.timer.start(1)

        self.cronometro = QtCore.QTimer(self.MainWindow)
        self.MainWindow.connect(self.cronometro, QtCore.SIGNAL('timeout()'), self.contar)

    def show_frame(self):
        # Tomamos una captura desde la webcam.
        ipl_image = self.camaraOjo.getImagen()
        ipl_image2 = self.camaraEscena.getImagen()

        if (self.capturing):
            self.out.write(ipl_image)
            self.out2.write(ipl_image2)
            # print "grabando frame"

        cv2.rectangle(ipl_image, (200, 140), (440, 340), (255, 0, 0), 2)

        # Leemos los pixeles de la imagen(numero_de_bytes_por_pixels * ancho * alto).
        data = cv2.cvtColor(ipl_image, cv2.cv.CV_BGR2RGB)
        data2 = cv2.cvtColor(ipl_image2, cv2.cv.CV_BGR2RGB)

        # Creamos una imagen a partir de los datos.
        #
        # QImage
        # (
        #   Los pixeles que conforman la imagen,
        #   Ancho de de la imagen,
        #   Alto de de la imagen,
        #   Numero de bytes que conforman una linea (numero_de_bytes_por_pixels * ancho),
        #   Formato de la imagen
        # )
        image = QtGui.QImage(data, data.shape[1], data.shape[0], data.strides[0], QtGui.QImage.Format_RGB888)
        image2 = QtGui.QImage(data2, data2.shape[1], data2.shape[0], data2.strides[0], QtGui.QImage.Format_RGB888)

        # Mostramos el QPixmap en la QLabel.
        self.MainWindow.lblCamOjo.setPixmap(QtGui.QPixmap.fromImage(image))
        self.MainWindow.lblCamEscena.setPixmap(QtGui.QPixmap.fromImage(image2))

    def contar(self):

        self.seg += 1
        if self.seg == 60:
            self.seg = 0
            self.min += 1
        if self.min == 60:
            self.min = 0
            self.hrs += 1
        if self.hrs == 24:
            self.hrs = 0

        self.MainWindow.lblhrs.setText(str(self.hrs))
        self.MainWindow.lblmin.setText(str(self.min))
        self.MainWindow.lblseg.setText(str(self.seg))

        print self.hrs, ": ", self.min, ": ", self.seg

    def volver(self):
        # self.newWindow = Welcome()
        # self.newWindow.WelcomeWindow.show()
        self.MainWindow.close()
        print 'LOL ATRAS'

    def iniciarGrabacion(self):
        print "iniciar grabacion ... "
        self.fourcc = cv2.cv.CV_FOURCC('i', 'Y', 'U', 'V')
        self.out = cv2.VideoWriter("Videos/ojo1.avi", self.fourcc, 20.0, (640, 480))
        self.out2 = cv2.VideoWriter("Videos/escena1.avi", self.fourcc, 20.0, (640, 480))
        self.capturing = True
        self.cronometro.start(1000)

    def terminarGrabacion(self):
        print "terminar grabacion"
        self.capturing = False
        self.cronometro.stop()
        self.mseg = 0
        self.seg = 0
        self.min = 0
        self.hrs = 0
        self.out = None
        self.out2 = None
        #self.out.release()
        # cv.ReleaseVideoWriter(self.out)
        #self.out2.release()
        # cv.ReleaseVideoWriter(self.out2)

    def analizarVideo(self):
        #self.progress.start(1)
        #self.hilo.start()

        self.procesa = Procesamiento()
        print "inicia analizando video..."

        #self.MainWindow.lblProcess.setText('Extrayendo frames...')
        self.procesa.getFrames('Videos/ojo1.avi', 'framesOjo/')
        self.completed += 25
        self.MainWindow.progBar.setValue(self.completed)

        #self.MainWindow.lblProcess.setText('Detectando y marcando pupilas...')
        self.procesa.marcarPupilas("Videos/pupila.avi", 'framesOjo/', "framesPupila/")
        self.completed += 25
        self.MainWindow.progBar.setValue(self.completed)

        #self.MainWindow.lblProcess.setText('Extrayendo frames...')
        self.procesa.getFrames('Videos/escena1.avi', 'framesEscena/')
        self.completed += 25
        self.MainWindow.progBar.setValue(self.completed)

        #self.MainWindow.lblProcess.setText('Marcando trayectoria...')
        self.procesa.marcarTrayectoria("Videos/trayectoria.avi", 'framesEscena/', "framesTrayectoria/")
        self.completed += 25
        self.MainWindow.progBar.setValue(self.completed)

        """self.getFrames('Videos/ojo1.avi', 'framesOjo/')
        self.marcarPupilas("Videos/pupila.avi", 'framesOjo/', "framesPupila/")
        self.getFrames('Videos/escena1.avi', 'framesEscena/')
        self.marcarTrayectoria("Videos/trayectoria.avi", 'framesEscena/', "framesTrayectoria/")"""



        print "termina analizando video..."



        #print "center points: ", self.procesa.center_points
        #print "center points size: ", len(self.procesa.center_points)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainClass = Main()
    mainClass.MainWindow.show()
    app.exec_()
