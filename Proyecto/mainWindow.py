import sys
import cv2
import os
from db import DB
from video import Video
from camara import Camara
from sistema import Sistema
from PyQt4 import uic, QtGui, QtCore
from procesamiento import Procesamiento
from playerWindow import PlayerW
from PyQt4.QtCore import SIGNAL,Qt,QThread,pyqtSignal
from PyQt4.QtGui import QApplication
import time
import threading


class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)

class progressThread(QThread):
    # QtCore.Signal(int) # or pyqtSignal(int)
    progress_update = pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        # your logic here
        while 1:
            maxVal = 1 # NOTE THIS CHANGED to 1 since updateProgressBar was updating the value by 1 every time
           # self.progress_update.emit(maxVal) # self.emit(SIGNAL('PROGRESS'), maxVal)
            self.emit(SIGNAL('PROGRESS'), maxVal)
            print"aqui"
            # Tell the thread to sleep for 1 second and let other things run
            time.sleep(1)


class Main:
    def __init__(self,idVideo,idPrueba):
        # Cargamos la GUI desde el archivo UI.
        self.MainWindow = uic.loadUi('main.ui')

        self.idVideo = idVideo
        self.idPrueba = idPrueba
        self.rutaVideos = 'EyeTracking/Prueba'+str(self.idPrueba)+'/Videos/'
        self.rutaFrames = 'EyeTracking/Prueba'+str(self.idPrueba)+'/Frames/'
        self.nombreVideoOjo = self.rutaVideos + 'ojo.avi'
        self.nombreVideoEscena = self.rutaVideos + 'escena.avi'
        self.nombreVideoPupila = self.rutaVideos + 'pupila.avi'
        self.nombreVideoTray = self.rutaVideos + 'trayectoria.avi'
        self.rutaFramesOjo = self.rutaFrames + 'FramesOjo/'
        self.rutaFramesEscena = self.rutaFrames + 'FramesEscena/'
        self.rutaFramesPupila = self.rutaFrames + 'FramesPupila/'
        self.rutaFramesTray = self.rutaFrames + 'FramesTray/'

        self.capturing = False
        self.seg = 0
        self.min = 0
        self.hrs = 0
        self.analisis = False
        self.camaraOjo = Camara(0)
        self.camaraEscena = Camara(2)
        self.db = DB()

        self.MainWindow.lblhrs.setText("00")
        self.MainWindow.lblmin.setText("00")
        self.MainWindow.lblseg.setText("00")

        self.MainWindow.btnGrabar.clicked.connect(self.iniciarGrabacion)
        self.MainWindow.btnGuardar.clicked.connect(self.terminarGrabacion)
        self.MainWindow.btnAnalizar.clicked.connect(self.analizarVideo)
        self.MainWindow.btnResultados.clicked.connect(self.resultados)

        self.timer = QtCore.QTimer(self.MainWindow)
        self.MainWindow.connect(self.timer, QtCore.SIGNAL('timeout()'), self.show_frame)
        self.timer.start(1)

        self.cronometro = QtCore.QTimer(self.MainWindow)
        self.MainWindow.connect(self.cronometro, QtCore.SIGNAL('timeout()'), self.contar)


        self.progress_thread = progressThread()

        self.MainWindow.connect(self.progress_thread, SIGNAL('PROGRESS'), self.updateProgressBar)

        #self.progress_thread.start()


    def updateProgressBar(self, maxVal):
        self.MainWindow.progressBar.setValue(self.MainWindow.progressBar.value() + maxVal)
        if maxVal == 0:
            self.MainWindow.progressBar.setValue(100)

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

    def iniciarGrabacion(self):
        print "iniciar grabacion ... "
        self.fourcc = cv2.cv.CV_FOURCC('i', 'Y', 'U', 'V')

        print "nombre video ojo ", self.nombreVideoOjo
        print "nombre video ojo ", self.nombreVideoEscena

        self.out = cv2.VideoWriter(self.nombreVideoOjo, self.fourcc, 20.0, (640, 480))
        self.out2 = cv2.VideoWriter(self.nombreVideoEscena, self.fourcc, 20.0, (640, 480))

        self.videoOjo = Video(self.idVideo,self.nombreVideoOjo,self.rutaFramesOjo,'ojo',self.idPrueba)
        self.videoEscena = Video(self.idVideo+1,self.nombreVideoEscena,self.rutaFramesEscena,'escena',self.idPrueba)

        if self.db.insertVideo(self.videoOjo):
            print 'Video insertado exitosamente'
        else:
            print 'Error al insertar video'

        if self.db.insertVideo(self.videoEscena):
            print 'Video insertado exitosamente'
        else:
            print 'Error al insertar video'


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

    def analizarVideo(self):

        """progress = QtGui.QProgressDialog("Analizando ...","Cancelar", 0, 100, self.MainWindow)
        progress.setCancelButton(None)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setAutoReset(True)
        progress.setAutoClose(True)
        progress.setMinimum(0)
        progress.setMaximum(100)
        progress.resize(400, 110)
        progress.setWindowTitle("Analisis")
        progress.show()"""
        self.analisis = True
        self.MainWindow.lblProcess.setText("Analizando...")
        self.MainWindow.progressBar.setValue(20)
        self.procesa = Procesamiento(self.idVideo, self.idPrueba)
        print "inicia analizando video..."
        #self.progress_thread.start()

        """self.procesa.marcarPupilas(self.nombreVideoOjo, self.nombreVideoPupila, self.rutaFramesOjo,
                                   self.rutaFramesPupila)
        #progress.setValue(50)
        self.procesa.marcarTrayectoria(self.nombreVideoEscena, self.nombreVideoTray, self.rutaFramesEscena,
                                       self.rutaFramesTray)"""

        t1 = FuncThread(self.procesa.marcarPupilas, self.nombreVideoOjo, self.nombreVideoPupila, self.rutaFramesOjo,
                                   self.rutaFramesPupila)
        t1.start()
        t1.join()
        self.MainWindow.progressBar.setValue(50)
        t2 = FuncThread(self.procesa.marcarTrayectoria, self.nombreVideoEscena, self.nombreVideoTray, self.rutaFramesEscena,
                                       self.rutaFramesTray)
        t2.start()
        t2.join()
        self.MainWindow.progressBar.setValue(100)
        self.analisis = False

        #progress.setValue(100)

        print "termina analizando video..."
        # progress.setValue(0)
        # progress.setValue(20)
        # progress.setValue(100)
        #progress.hide()

    def resultados(self):
        self.resultadosWindow = PlayerW(self.idPrueba)
        self.resultadosWindow.PlayerWindow.show()
        #self.camaraOjo.liberarCamara()
        #self.camaraEscena.liberarCamara()
        self.MainWindow.close()
        app.closingDown()
        #self.progress_thread.start()


if __name__ == "__main__":

    db = DB()
    lastVideo = db.getTheLastVideo()

    idVideo = lastVideo.idVideo + 1
    idPrueba = lastVideo.idPrueba + 1

    print "idVideo: ",idVideo
    print "idPrueba: ",idPrueba

    sistema = Sistema()
    sistema.createDirectory('EyeTracking/Prueba'+str(idPrueba))
    sistema.createDirectory('EyeTracking/Prueba'+str(idPrueba)+'/Videos')
    sistema.createDirectory('EyeTracking/Prueba'+str(idPrueba)+'/Frames')
    sistema.createDirectory('EyeTracking/Prueba'+str(idPrueba)+'/Frames/FramesOjo')
    sistema.createDirectory('EyeTracking/Prueba'+str(idPrueba)+'/Frames/FramesEscena')
    sistema.createDirectory('EyeTracking/Prueba'+str(idPrueba)+'/Frames/FramesPupila')
    sistema.createDirectory('EyeTracking/Prueba'+str(idPrueba)+'/Frames/FramesTray')

    app = QtGui.QApplication(sys.argv)
    mainClass = Main(idVideo,idPrueba)
    mainClass.MainWindow.show()
    app.exec_()

