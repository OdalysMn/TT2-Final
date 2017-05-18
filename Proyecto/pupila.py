
class Pupila:
    def __init__(self, idPupila, coordenadaX, coordenadaY, tiempo, idFrame, numberOfFrame):
        self.idPupila = idPupila
        self.coordenadaX = coordenadaX
        self.coordenadaY = coordenadaY
        self.tiempo = tiempo
        self.idFrame = idFrame
        self.numberOfFrame = numberOfFrame

    def strPupila(self):
        return "%s %s %s %s %s %s" % (self.idPupila,self.coordenadaX,self.coordenadaY,self.tiempo,self.idFrame,self.numberOfFrame)

