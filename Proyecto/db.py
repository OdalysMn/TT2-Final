import MySQLdb
from video import Video
from frame import Frame
from pupila import Pupila

class db:
    def __init__(self):
        self.db = MySQLdb.connect("localhost", "root", "", "tt2")
        self.cursor = self.db.cursor()

    def getTheLasIdVideo(self):
        # Preparamos el query SQL para obtener todos los empleados de la BD
        id_Video = 0
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

    
