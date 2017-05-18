import sys
import cv2
from db import DB
from player import Player
from PyQt4 import uic, QtGui, QtCore


class PlayerW:
    def __init__(self,idPrueba):
        # Cargamos la GUI desde el archivo UI.
        self.PlayerWindow = uic.loadUi('player.ui')
        self.rutaVideos = 'EyeTracking/Prueba'+str(idPrueba)+'/Videos/'
        self.nombreVideoPupila = self.rutaVideos + 'pupila.avi'
        self.nombreVideoTray = self.rutaVideos + 'trayectoria.avi'
        self.videoPupila = cv2.VideoCapture(self.nombreVideoPupila)
        self.videoTray = cv2.VideoCapture(self.nombreVideoTray)

        self.PlayerWindow.btnReproducir.clicked.connect(self.playVideo)


        #self.timer = QtCore.QTimer( self.PlayerWindow)
        #self.PlayerWindow.connect(self.timer, QtCore.SIGNAL('timeout()'), self.show_frame)
        #self.timer.start(1)

    def show_frame(self,frame1,frame2):
        # Tomamos una captura desde la webcam.

        ipl_image = frame1
        ipl_image2 = frame2

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
        self.PlayerWindow.lblCamOjo.setPixmap(QtGui.QPixmap.fromImage(image))
        self.PlayerWindow.lblCamEscena.setPixmap(QtGui.QPixmap.fromImage(image2))

    def playVideo(self):
        while (self.videoPupila.isOpened()):
            ret, frame1 = self.videoPupila.read()
            ret1, frame2 = self.videoTray.read()


            if ret == True & ret1 == True:
                cv2.imshow('frame1', frame1)
                cv2.imshow('frame2', frame2)

                self.show_frame(frame1,frame2)


            else:
                break

        self.videoPupila.release()
        self.videoTray.release()
        cv2.destroyAllWindows()




if __name__ == "__main__":
    db = DB()
    lastVideo = db.getTheLastVideo()

    idPrueba = lastVideo.idPrueba

    print "idPrueba: ", idPrueba

    app = QtGui.QApplication(sys.argv)
    player = PlayerW(idPrueba)
    player.PlayerWindow.show()
    app.exec_()