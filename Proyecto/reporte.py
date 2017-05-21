import sys
import os
from reportlab.pdfgen import canvas
from db import DB
from PyQt4 import uic, QtGui
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader


class Reporte:
    def __init__(self,idPrueba):
        # Cargamos la GUI desde el archivo UI.
        self.ReporteWindow = uic.loadUi('reporte.ui')
        self.rutaReporte = 'EyeTracking/Prueba'+str(idPrueba)+'/Reporte.pdf'
        self.rutaDatos = 'EyeTracking/Prueba'+str(idPrueba)+'/trayectoria.txt'
        self.data = self.readData()
        self.ReporteWindow.txtNombrePrueba.setText('Prueba '+str(idPrueba))
        self.lista = self.data[len(self.data)-1]
        self.ReporteWindow.txtDuracionPrueba.setText(str(self.lista[len(self.lista)-2]))

        self.ReporteWindow.btnPDF.clicked.connect(self.generatePDF)

    def readData(self):
        data = []

        # En primer lugar debemos de abrir el fichero que vamos a leer.
        # Usa 'rb' en vez de 'r' si se trata de un fichero binario.
        infile = open(self.rutaDatos, 'r')
        # Mostramos por pantalla lo que leemos desde el fichero
        #print('>>> Lectura del fichero linea a linea')
        for line in infile:
            data.append(line.split(','))
        # Cerramos el fichero.
        infile.close()

        #print 'data: ',data

        return data

    def drawTable(self,inicio,fin):

        subdata = []
        subdata.append(['Fijacion', 'Coordenada X', 'Coordenada Y', 'Tiempo', 'Frame'])
        i = inicio
        while i < fin:
            subdata.append(self.data[i])
            i += 1

        print "len subdata: ", len(subdata)
        if len(subdata) == 41:
            x=6
            y=50
        else:
            x=6
            y=200

        style = TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                            ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
                            ('VALIGN', (0, 0), (0, -1), 'TOP'),
                            ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
                            ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                            ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
                            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                            ])

        # Configure style and word wrap
        s = getSampleStyleSheet()
        s = s["BodyText"]
        s.wordWrap = 'CJK'
        data2 = [[Paragraph(cell, s) for cell in row] for row in subdata]
        t = Table(data2)
        t.setStyle(style)
        t.wrapOn(self.c, 50, 50)
        t.drawOn(self.c, x, y)

        self.c.showPage()
        self.c.save()

        return fin


    def generatePDF(self):

        # Guardo en las variables los datos de los textEdit Ingresados por el Usuario
        self.nombrePrueba = str(self.ReporteWindow.txtNombrePrueba.text())
        self.duracionPrueba = str(self.ReporteWindow.txtDuracionPrueba.text())
        self.descripcionPrueba = str(self.ReporteWindow.txtDescripcionPrueba.toPlainText())

        # Ruta donde quiero crear el PDF
        self.c = canvas.Canvas(self.rutaReporte,pagesize=A4)
        self.c.drawImage('C:/Users/Odalys/Documents/ESCOM/TT2/TT2/resources/logoipn.png', 10, 700, 100, 100, mask='auto')
        self.c.drawImage('C:/Users/Odalys/Documents/ESCOM/TT2/TT2/resources/logoescom.png', 480, 700, 100, 100, mask='auto')
        self.c.drawString(200, 750, "Herramienta Eye Tracking para la")
        self.c.drawString(250, 730, "Investigacion")
        self.c.drawString(250, 690, "REPORTE")

        self.c.drawString(100, 650, ("Nombre de la Prueba: " + self.nombrePrueba))
        self.c.drawString(100, 630, ("Duracion de la Prueba: " + self.duracionPrueba))
        self.c.drawString(100, 610, "Descripcion de la Prueba: ")
        #self.c.drawString(100, 590, self.descripcionPrueba)
        styles = getSampleStyleSheet()
        styleN = styles['Normal']

        P = Paragraph(self.descripcionPrueba,styleN)
        P.wrap(400, 50)
        P.drawOn(self.c, 100, 430)
        #self.c.showPage()
        self.c.drawString(100, 410, "Trayectoria Final ")
        rutaImagenTrayectoria = "C:/Users/Odalys/Documents/ESCOM/TT2/TT2/Proyecto/"+str(self.lista[len(self.lista)-1])
        rutaT = rutaImagenTrayectoria.replace("\n", "")
        imagen = ImageReader(rutaT)
        self.c.drawImage(imagen, 20, 80, 550, 300, mask='auto')

        self.c.showPage()
        self.c.drawString(100, 800, "Tabla de Fijaciones ")

        inicio = 0
        fin = 40

        limit = (len(self.data)-1)/40.0
        print "limit: ", limit
        limit=round(limit,0)
        print "limit: ",limit
        i=0

        while i < limit:

            ultimo = self.drawTable(inicio,fin)
            print "ultimo: ", ultimo
            inicio = ultimo
            fin = ultimo + 40
            if fin > len(self.data):
                fin = len(self.data)
            i+=1





        # PARA LINUX: os.system("evince /home/diego123/Escritorio/Formulario.pdf &")
        os.system("start AcroRD32 "+self.rutaReporte+" &")



if __name__ == "__main__":
    db = DB()
    lastVideo = db.getTheLastVideo()

    idPrueba = lastVideo.idPrueba

    print "idPrueba: ", idPrueba

    app = QtGui.QApplication(sys.argv)
    reporte = Reporte(idPrueba)
    reporte.ReporteWindow.show()
    app.exec_()