import sys
import os
from reportlab.pdfgen import canvas
from db import DB
from PyQt4 import uic, QtGui, QtCore


class Reporte:
    def __init__(self,idPrueba):
        # Cargamos la GUI desde el archivo UI.
        self.ReporteWindow = uic.loadUi('reporte.ui')
        self.rutaReporte = 'EyeTracking/Prueba'+str(idPrueba)+'/Reporte.pdf'
        self.ReporteWindow.txtNombrePrueba.setText('Prueba '+str(idPrueba))
        self.ReporteWindow.txtDuracionPrueba.setText('00hr:00min:00s')


        self.ReporteWindow.btnPDF.clicked.connect(self.generatePDF)


    def generatePDF(self):
        # Guardo en las variables los datos de los textEdit Ingresados por el Usuario
        self.nombrePrueba = str(self.ReporteWindow.txtNombrePrueba.text())
        self.duracionPrueba = str(self.ReporteWindow.txtDuracionPrueba.text())
        self.descripcionPrueba = str(self.ReporteWindow.txtDescripcionPrueba.toPlainText())


        # Ruta donde quiero crear el PDF
        c = canvas.Canvas(self.rutaReporte)
        c.drawString(100, 750, "Este formulario fue creado en www.pythondiario.com")
        c.drawString(100, 700, ("Nombre de la Prueba: " + self.nombrePrueba))
        c.drawString(100, 680, ("Duracion de la Prueba: " + self.duracionPrueba))
        c.drawString(100, 660, ("Descripcion de la Prueba: " + self.descripcionPrueba))

        c.save()

        # PARA WINDOWS: os.system("start AcroRD32 ruta_y_archivo.pdf &")
        os.system("start AcroRD32 "+ self.rutaReporte+" &")

if __name__ == "__main__":
    db = DB()
    lastVideo = db.getTheLastVideo()

    idPrueba = lastVideo.idPrueba

    print "idPrueba: ", idPrueba

    app = QtGui.QApplication(sys.argv)
    reporte = Reporte(idPrueba)
    reporte.ReporteWindow.show()
    app.exec_()