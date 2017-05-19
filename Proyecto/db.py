import MySQLdb
from video import Video
from frame import Frame
from pupila import Pupila

class DB:
    def __init__(self):
        self.db = MySQLdb.connect("localhost", "root", "", "tt2")
        self.cursor = self.db.cursor()

    def getTheLastVideo(self):
        # Preparamos el query SQL para obtener todos los empleados de la BD
        video = Video(0,'','','',0)
        sql = "SELECT * FROM videos WHERE id_Video=(SELECT MAX(id_Video) FROM videos)"

        try:
            # Ejecutamos el comando
            self.cursor.execute(sql)
            # Obtenemos todos los registros en una lista de listas
            resultados = self.cursor.fetchall()

            print "resultados: ",resultados

            if len(resultados) == 0:
                return video
            else:
                for registro in resultados:
                    video.idVideo = registro[0]
                    video.rutaVideo = registro[1]
                    video.rutaFrames = registro[2]
                    video.tipoVideo = registro[3]
                    video.idPrueba = registro[4]

                return video
        except:
            print "Error: No se pudieron obtener los datos"

    def getTheLastFrame(self):
        # Preparamos el query SQL para obtener todos los empleados de la BD
        frame = Frame(0,0,'',0)
        sql = "SELECT * FROM frames WHERE id_Frame=(SELECT MAX(id_Frame) FROM frames)"

        try:
            # Ejecutamos el comando
            self.cursor.execute(sql)
            # Obtenemos todos los registros en una lista de listas
            resultados = self.cursor.fetchall()

            print "resultados: ",resultados

            if len(resultados) == 0:
                return frame
            else:
                for registro in resultados:
                    frame.idFrame = registro[0]
                    frame.numberOfFrame = registro[1]
                    frame.rutaFrame = registro[2]
                    frame.idVideo = registro[3]

                return frame
        except:
            print "Error: No se pudieron obtener los datos"

    def getTheLastPupil(self):
        # Preparamos el query SQL para obtener todos los empleados de la BD
        pupil = Pupila(0,0,0,0,0,0)
        sql = "SELECT * FROM pupila WHERE id_Pupila=(SELECT MAX(id_Pupila) FROM pupila)"

        try:
            # Ejecutamos el comando
            self.cursor.execute(sql)
            # Obtenemos todos los registros en una lista de listas
            resultados = self.cursor.fetchall()

            print "resultados: ",resultados

            if len(resultados) == 0:
                return pupil
            else:
                for registro in resultados:
                    pupil.idPupila = registro[0]
                    pupil.coordenadaX = registro[1]
                    pupil.coordenadaY = registro[2]
                    pupil.tiempo = registro[3]
                    pupil.idFrame = registro[4]
                    pupil.numberOfFrame = registro[5]

                return pupil
        except:
            print "Error: No se pudieron obtener los datos"

    def insertVideo(self,video):
        try:
            # Ejecutamos el comando
            self.cursor.execute(
                "INSERT INTO videos (id_Video,ruta_Video, ruta_Frames, tipo_Video, idPrueba) VALUES (%s, %s, %s, %s, %s)",
                (video.idVideo, video.rutaVideo, video.rutaFrames, video.tipoVideo, video.idPrueba))
            # Efectuamos los cambios en la base de datos
            self.db.commit()
            return True

        except:
            # Si se genero algun error revertimos la operacion
            self.db.rollback()
            return False

    def insertFrame(self,frame):
        try:
            # Ejecutamos el comando
            self.cursor.execute(
                "INSERT INTO frames (id_Frame,number_of_Frame, ruta_Frame, id_Video) VALUES (%s, %s, %s, %s)",
                (frame.idFrame, frame.numberOfFrame, frame.rutaFrame, frame.idVideo))
            # Efectuamos los cambios en la base de datos
            self.db.commit()
            return True

        except:
            # Si se genero algun error revertimos la operacion
            self.db.rollback()
            return False

    def getFrames(self,idVideo):

        idFrames = []
        try:
            # Ejecutamos el comando
            self.cursor.execute("SELECT * FROM frames WHERE id_Video = %s",(idVideo))
            # Obtenemos todos los registros en una lista de listas
            resultados = self.cursor.fetchall()

            for registro in resultados:

                idFrames.append(registro[0])

            return idFrames
        except:

            return idFrames

    def insertPupila(self,pupila):
        try:
            # Ejecutamos el comando
            self.cursor.execute(
                "INSERT INTO pupila (id_Pupila,coordenadaX, coordenadaY, tiempo,id_Frame,number_of_Frame) VALUES (%s,%s,%s,%s,%s,%s)",
                (pupila.idPupila, pupila.coordenadaX, pupila.coordenadaY, pupila.tiempo, pupila.idFrame, pupila.numberOfFrame))
            # Efectuamos los cambios en la base de datos
            self.db.commit()
            return True

        except:
            # Si se genero algun error revertimos la operacion
            self.db.rollback()
            return False

    def getPupil(self,idFrame):

        pupil = []
        try:
            # Ejecutamos el comando
            self.cursor.execute("SELECT * FROM pupila WHERE id_Frame = %s", (idFrame))
            # Obtenemos todos los registros en una lista de listas
            resultados = self.cursor.fetchall()

            for registro in resultados:
                p = Pupila(registro[0], registro[1], registro[2], registro[3],registro[4],registro[5])
                pupil.append(p)

            return pupil
        except:

            return pupil

db = DB()

"""id = db.getTheLasIdVideo()

print "id: ",id

video = Video(0,'C:/video1','C:/framesVideo1','pupila',1)
frame = Frame(0,0,'C:/framesVideo1/0.jpg',0)
pupila = Pupila(1,258,369,1.5,0,0)

db = DB()

res = db.getFrames(frame.idVideo)
print 'res.legth: ',len(res)

for r in res:
    print 'r: ',r.strFrame()

res = db.getPupil(frame.idFrame)
print 'res.legth: ',len(res)

for r in res:
    print 'r: ',r.strPupila()

if db.insertVideo(video):
    print 'Insertado con exito'
else:
    print 'Error al insertar'

if db.insertFrame(frame):
    print 'Insertado con exito'
else:
    print 'Error al insertar'

if db.insertPupila(pupila):
    print 'Insertado con exito'
else:
    print 'Error al insertar'"""

"""count = 0
while count<100:
    frame = Frame(count+1, 0, 'C:/framesVideo1/0.jpg', 7)
    if db.insertFrame(frame):
        print 'Insertado con exito'
    else:
        print 'Error al insertar'
    count +=1

db = DB()

idFrames = db.getFrames(3)

for idf in idFrames:
    print "idFrame: ",idf"""


