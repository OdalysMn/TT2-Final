import sys
import cv2
import cv
import time
from PyQt4 import uic, QtGui, QtCore
from camara import Camara
import numpy as np

class Procesamiento:
    def __init__(self):
        self.center_points = []

    def getFrames(self, rutaVideo, rutaFrames):
        self.cap = cv2.VideoCapture(rutaVideo)
        self.totalFrames = 0

        while (self.cap.isOpened()):

            ret, frame = self.cap.read()
            if ret == True:

                # write the frame
                cv2.imwrite(rutaFrames + "frame%d.jpg" % self.totalFrames, frame)  # save frame as JPEG file
                self.totalFrames += 1
                print self.totalFrames

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        # Release everything if job is finished
        self.cap.release()

    def detecPupil(self, name):
        centers = []

        image = cv2.imread(name)
        frame = cv2.flip(image, 1)

        gray = cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)

        retval, thresholded = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        closed = cv2.erode(cv2.dilate(thresholded, kernel, iterations=1), kernel, iterations=1)
        contours, hierarchy = cv2.findContours(closed, cv2.cv.CV_RETR_LIST, cv2.cv.CV_CHAIN_APPROX_NONE)

        drawing = np.copy(frame)

        for contour in contours:
            contour = cv2.convexHull(contour)
            area = cv2.contourArea(contour)

            if area < 400:
                continue

            bounding_box = cv2.boundingRect(contour)

            extend = area / (bounding_box[2] * bounding_box[3])

            # reject the contours with big extend
            if extend > 0.8:
                continue

            # calculate countour center and draw a dot there
            m = cv2.moments(contour)

            if m['m00'] != 0:
                center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))


                cv2.circle(drawing, center, 4, 255, 2)
                print "antes: ",center

                lst = list(center)
                lst[0] = int(round(lst[0] * 1.454545, 0))
                lst[1] = int(round(lst[1] * 1.411764, 0))
                center = tuple(lst)

                centers.append(center)

                print "despues: ",center

                # fit an ellipse around the contour and draw it into the image
            points = len(contour)
            if points < 5:
                continue

            ellipse = cv2.fitEllipse(contour)
            cv2.ellipse(drawing, box=ellipse, color=255)

        print 'centers: ', centers
        if (len(centers) > 2):

            self.center_points.append(centers[len(centers) - 1])

        elif (len(centers) == 0):
            self.center_points.append([291, 232])
        else:
            self.center_points.append(centers[0])

        return drawing

    def marcarPupilas(self, rutaVideo, rutaFramesLeer, rutaFramesGuardar):
        fourcc = cv2.cv.CV_FOURCC('i', 'Y', 'U', 'V')
        out = cv2.VideoWriter(rutaVideo, fourcc, 20.0, (640, 480))
        count = 0

        while (count < self.totalFrames):
            name = rutaFramesLeer + 'frame' + str(count) + '.jpg'

            pupilImage = self.detecPupil(name)

            cv2.imwrite(rutaFramesGuardar + "frame%d.jpg" % count, pupilImage)  # save frame as JPEG file
            count += 1
            print count

            out.write(pupilImage)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

                # out.release()

    def drawCoordinate(self, nombre_frame, points):
        image = cv2.imread(nombre_frame)

        line_coordinates = []

        for point in points:
            cv2.circle(image, tuple(point), 18, 255, -1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, str(points.index(point)), tuple(point), font, 1, (255, 255, 255), 1, 255)
            line_coordinates.append(tuple(point))
            # print tuple(point)

        # print line_coordinates

        for t in range(len(line_coordinates) - 1):
            #    print line_coordinates[t], line_coordinates[t + 1]
            cv2.line(image, line_coordinates[t], line_coordinates[t + 1], 255, 1)

        return image

    def marcarTrayectoria(self, rutaVideo, rutaFramesLeer, rutaFramesGuardar):

        count = 0
        fourcc = cv2.cv.CV_FOURCC('i', 'Y', 'U', 'V')
        out = cv2.VideoWriter(rutaVideo, fourcc, 20.0, (640, 480))

        while count < self.totalFrames:

            points = []
            count2 = 0
            print count
            while count2 < count:
                # print "Tupla: ", self.center_points[count2]

                points.append(self.center_points[count2])
                count2 = count2 + 1

            pupilImage = self.drawCoordinate(rutaFramesLeer + 'frame' + str(count) + '.jpg', points)
            cv2.imwrite(rutaFramesGuardar + "frametray%d.jpg" % count, pupilImage)
            out.write(pupilImage)

            count = count + 1

class Hilo(QtCore.QThread):
    def __init__(self,val, parent = None):
        super(Hilo,self).__init__(parent)
        self.val = val

    def run(self):
        while(self.val < 100):
            self.val = self.val + 1
            self.emit(QtCore.SIGNAL('VALUE'),self.val)



class GUI:
    def __init__(self):
        # Cargamos la GUI desde el archivo UI.
        self.MainWindow = uic.loadUi('main.ui')

        self.capturing = False
        self.mseg = 0
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

        self.progress = QtCore.QTimer(self.MainWindow)
        self.MainWindow.connect(self.progress, QtCore.SIGNAL('timeout()'), self.llenarBarra)

        self.cronometro = QtCore.QTimer(self.MainWindow)
        self.MainWindow.connect(self.cronometro, QtCore.SIGNAL('timeout()'), self.contar)

        self.hilo = Hilo(0)
        #self.hilo.start()
        self.MainWindow.connect(self.hilo,QtCore.SIGNAL('VALUE'),self.updateProgressBar)

    def updateProgressBar(self,val):
        self.MainWindow.progBar.setValue(val)


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

    def getFrames(self, rutaVideo, rutaFrames):

        self.cap = cv2.VideoCapture(rutaVideo)
        self.totalFrames = 0
        self.completed = 0
        self.MainWindow.lblProcess.setText('Extrayendo frames...')
        while (self.cap.isOpened()):

            ret, frame = self.cap.read()
            if ret == True:

                # write the frame
                cv2.imwrite(rutaFrames + "frame%d.jpg" % self.totalFrames, frame)  # save frame as JPEG file
                self.totalFrames += 1
                print self.totalFrames
                self.completed += 1
                self.MainWindow.progBar.setValue(self.completed)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        # Release everything if job is finished
        self.cap.release()

    def detecPupil(self, name):
        centers = []

        image = cv2.imread(name)
        frame = cv2.flip(image, 1)

        gray = cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)

        retval, thresholded = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        closed = cv2.erode(cv2.dilate(thresholded, kernel, iterations=1), kernel, iterations=1)
        contours, hierarchy = cv2.findContours(closed, cv2.cv.CV_RETR_LIST, cv2.cv.CV_CHAIN_APPROX_NONE)

        drawing = np.copy(frame)

        for contour in contours:
            contour = cv2.convexHull(contour)
            area = cv2.contourArea(contour)

            if area < 400:
                continue

            bounding_box = cv2.boundingRect(contour)

            extend = area / (bounding_box[2] * bounding_box[3])

            # reject the contours with big extend
            if extend > 0.8:
                continue

            # calculate countour center and draw a dot there
            m = cv2.moments(contour)

            if m['m00'] != 0:
                center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))


                cv2.circle(drawing, center, 4, 255, 2)
                print "antes: ",center

                lst = list(center)
                lst[0] = int(round(lst[0] * 1.454545, 0))
                lst[1] = int(round(lst[1] * 1.411764, 0))
                center = tuple(lst)

                centers.append(center)

                print "despues: ",center

                # fit an ellipse around the contour and draw it into the image
            points = len(contour)
            if points < 5:
                continue

            ellipse = cv2.fitEllipse(contour)
            cv2.ellipse(drawing, box=ellipse, color=255)

        print 'centers: ', centers
        if (len(centers) > 2):

            self.center_points.append(centers[len(centers) - 1])

        elif (len(centers) == 0):
            self.center_points.append([291, 232])
        else:
            self.center_points.append(centers[0])

        return drawing

    def marcarPupilas(self, rutaVideo, rutaFramesLeer, rutaFramesGuardar):
        fourcc = cv2.cv.CV_FOURCC('i', 'Y', 'U', 'V')
        out = cv2.VideoWriter(rutaVideo, fourcc, 20.0, (640, 480))
        count = 0
        self.completed = 0
        self.MainWindow.lblProcess.setText('Detectando y marcando pupilas...')

        while (count < self.totalFrames):
            name = rutaFramesLeer + 'frame' + str(count) + '.jpg'

            pupilImage = self.detecPupil(name)

            cv2.imwrite(rutaFramesGuardar + "frame%d.jpg" % count, pupilImage)  # save frame as JPEG file
            count += 1
            self.completed += 1
            self.MainWindow.progBar.setValue(self.completed)
            print count

            out.write(pupilImage)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

                # out.release()

    def drawCoordinate(self, nombre_frame, points):
        image = cv2.imread(nombre_frame)

        line_coordinates = []

        for point in points:
            cv2.circle(image, tuple(point), 18, 255, -1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, str(points.index(point)), tuple(point), font, 1, (255, 255, 255), 1, 255)
            line_coordinates.append(tuple(point))
            # print tuple(point)

        # print line_coordinates

        for t in range(len(line_coordinates) - 1):
            #    print line_coordinates[t], line_coordinates[t + 1]
            cv2.line(image, line_coordinates[t], line_coordinates[t + 1], 255, 1)

        return image

    def marcarTrayectoria(self, rutaVideo, rutaFramesLeer, rutaFramesGuardar):

        count = 0
        fourcc = cv2.cv.CV_FOURCC('i', 'Y', 'U', 'V')
        out = cv2.VideoWriter(rutaVideo, fourcc, 20.0, (640, 480))
        self.completed = 0
        self.MainWindow.lblProcess.setText('Marcando trayectoria...')

        while count < self.totalFrames:

            points = []
            count2 = 0
            print count
            while count2 < count:
                # print "Tupla: ", self.center_points[count2]

                points.append(self.center_points[count2])
                count2 = count2 + 1

            pupilImage = self.drawCoordinate(rutaFramesLeer + 'frame' + str(count) + '.jpg', points)
            cv2.imwrite(rutaFramesGuardar + "frametray%d.jpg" % count, pupilImage)
            out.write(pupilImage)

            count = count + 1
            self.completed += 1
            self.MainWindow.progBar.setValue(self.completed)

    def contar(self):

        self.seg = self.seg + 1
        if (self.seg == 60):
            self.seg = 0
            self.min = self.min + 1
        if (self.min == 60):
            self.min = 0
            self.hrs = self.hrs + 1
        if (self.hrs == 24):
            self.hrs = 0

        self.MainWindow.lblhrs.setText(str(self.hrs))
        self.MainWindow.lblmin.setText(str(self.min))
        self.MainWindow.lblseg.setText(str(self.seg))

        print self.hrs, ": ", self.min, ": ", self.seg

    def llenarBarra(self):

        print "llenar barra"

        if self.completed < 100:

            self.completed += 1
            self.MainWindow.progBar.setValue(self.completed)

            print "self.completed value: ",self.completed

        else:
            self.progress.stop()


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
    gui = GUI()
    gui.MainWindow.show()
    app.exec_()
