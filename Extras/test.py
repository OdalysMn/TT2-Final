import cv2
from PyQt4 import QtGui, QtCore




class Capture():
    def __init__(self):
        self.capturing = False
        self.c = cv2.VideoCapture(0)
        self.c2 = cv2.VideoCapture(2)


    def startCapture(self):
        print "pressed start"
        self.capturing = True
        cap = self.c
        cap2 = self.c2

        self.fourcc = cv2.cv.CV_FOURCC('i', 'Y', 'U', 'V')
        self.out = cv2.VideoWriter('ojo1.avi', self.fourcc, 20.0, (640,480))
        self.out2 = cv2.VideoWriter('escena1.avi', self.fourcc, 20.0, (640, 480))

        while(self.capturing):
            ret, frame = cap.read()
            ret2, frame2 = cap2.read()
            cv2.imshow("Ojo", frame)
            cv2.imshow("Escena", frame2)

            self.out.write(frame)
            self.out2.write(frame2)
            cv2.waitKey(5)
        cv2.destroyAllWindows()

    def endCapture(self):
        print "pressed End"
        self.capturing = False

    def quitCapture(self):
        print "pressed Quit"
        cap = self.c
        cap2 = self.c2
        cv2.destroyAllWindows()
        cap.release()
        cap2.release()
        QtCore.QCoreApplication.quit()


class Window(QtGui.QWidget):
    def __init__(self):

        QtGui.QWidget.__init__(self)
        self.setWindowTitle('Control Panel')

        self.capture = Capture()
        self.start_button = QtGui.QPushButton('Start',self)
        self.start_button.clicked.connect(self.capture.startCapture)

        self.end_button = QtGui.QPushButton('End',self)
        self.end_button.clicked.connect(self.capture.endCapture)

        self.quit_button = QtGui.QPushButton('Quit',self)
        self.quit_button.clicked.connect(self.capture.quitCapture)

        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.end_button)
        vbox.addWidget(self.quit_button)

        self.setLayout(vbox)
        self.setGeometry(100,100,200,200)
        self.show()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())