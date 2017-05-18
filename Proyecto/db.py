import MySQLdb
from video import Video
from frame import Frame
from pupila import Pupila

class DB:
    def __init__(self):
        self.db = MySQLdb.connect("localhost", "root", "", "tt2")
        self.cursor = self.db.cursor()

    def getTheLasIdVideo(self):
        # Preparamos el query SQL para obtener todos los empleados de la BD
        id_Video = 1
        sql = "SELECT * FROM videos WHERE id_Video=(SELECT MAX(id_Video) FROM videos)"

        try:
            # Ejecutamos el comando
            self.cursor.execute(sql)
            # Obtenemos todos los registros en una lista de listas
            resultados = self.cursor.fetchall()

            if len(resultados) == 0:
                return id_Video
            else:
                for registro in self.resultados:
                    id_Video = registro[0]
                return id_Video
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

        frames = []
        try:
            # Ejecutamos el comando
            self.cursor.execute("SELECT * FROM frames WHERE id_Video = %s",(idVideo))
            # Obtenemos todos los registros en una lista de listas
            resultados = self.cursor.fetchall()

            for registro in resultados:
                f = Frame(registro[0],registro[1],registro[2],registro[3])
                frames.append(f)

            return frames
        except:

            return frames

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

#video = Video(0,'C:/video1','C:/framesVideo1','pupila',1)
frame = Frame(0,0,'C:/framesVideo1/0.jpg',0)
#pupila = Pupila(1,258,369,1.5,0,0)

db = DB()

"""res = db.getFrames(frame.idVideo)
print 'res.legth: ',len(res)

for r in res:
    print 'r: ',r.strFrame()"""

res = db.getPupil(frame.idFrame)
print 'res.legth: ',len(res)

for r in res:
    print 'r: ',r.strPupila()

"""if db.insertVideo(video):
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
