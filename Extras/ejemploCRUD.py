import MySQLdb


class Empleado:

   def __init__(self,nombre,ap,edad,sexo,salario):
      self.nombre = nombre
      self.apellido = ap
      self.edad = edad
      self.sexo = sexo
      self.salario = salario


class CrudEmpleado:

   def __init__(self):

      self.db = MySQLdb.connect("localhost","root","","tt2" )
      self.cursor = self.db.cursor()

   def insertatEmpleado(self,empleado):

      try:
         # Ejecutamos el comando
         self.cursor.execute("INSERT INTO EMPLEADO (NOMBRE,APELLIDO, EDAD, SEXO, SALARIO) VALUES (%s, %s, %s, %s, %s)",
                              (empleado.nombre,empleado.apellido,empleado.edad,empleado.sexo,empleado.salario))
         # Efectuamos los cambios en la base de datos
         self.db.commit()
         print "insertado con exito"

      except:
         # Si se genero algun error revertamos la operacion
         self.db.rollback()
         print "error"

   def eliminarEmpleado(self,apellido):
      try:
         # Ejecutamos el comando
         self.cursor.execute("DELETE FROM EMPLEADO WHERE APELLIDO=%s",apellido)
         # Efectuamos los cambios en la base de datos
         self.db.commit()
         print "borrado con exito"

      except:
         # Si se genero algun error revertamos la operacion
         self.db.rollback()
         print "error"

   def traerEmpleados(self):
      # Preparamos el query SQL para obtener todos los empleados de la BD
      sql = "SELECT * FROM videos WHERE id_Video=(SELECT MAX(id_Video) FROM videos)"
      try:
         # Ejecutamos el comando
         self.cursor.execute(sql)
         # Obtenemos todos los registros en una lista de listas
         self.resultados = self.cursor.fetchall()

         print "resultados: ",self.resultados
         print "resultados size: ",len(self.resultados)

         #print "resultados: ",self.resultados
         for registro in self.resultados:
            id_Video = registro[0]
            ruta_Video = registro[1]
            ruta_Frames = registro[1]
            tipo_Video = registro[3]
            idPrueba = registro[4]

            # Imprimimos los resultados obtenidos
            print "id_Video=%d, ruta_Video=%s, ruta_Frames=%s, tipo_Video=%d, idPrueba=%d" % (id_Video,ruta_Video, ruta_Frames, tipo_Video, idPrueba)
      except:
         print "Error: No se pudieron obtener los datos"

   def modificarEmpleado(self,salario):

      try:
         # Ejecutamos el comando
         self.cursor.execute("UPDATE EMPLEADO SET EDAD = EDAD + 1 WHERE SALARIO = %s",(salario))
         # Efectuamos los cambios en la base de datos
         self.db.commit()
         print "modificado con exito"

      except:
         # Si se genero algun error revertamos la operacion
         self.db.rollback()
         print "error al modificar"


#persona = Empleado('Odalys','Marron',24,'F',10500)
#persona1 = Empleado('Maria','Castro',64,'F',22000)
#persona2 = Empleado('Homero','Simpson',48,'M',12000)
#persona3 = Empleado('Bob','Esponja',28,'M',16000)

crud = CrudEmpleado()
"""crud.insertatEmpleado(persona)
crud.insertatEmpleado(persona1)
crud.insertatEmpleado(persona2)
crud.insertatEmpleado(persona3)"""

#crud.eliminarEmpleado(persona.apellido)

crud.traerEmpleados()
#crud.modificarEmpleado(persona.salario)
