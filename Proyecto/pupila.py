
class Pupila:
    def __init__(self, idPupila, coordenadaX, coordenadaY, tiempo, idFrame, numberOfFrame):
        self.idPupila = idPupila
        self.coordenadaX = coordenadaX
        self.coordenadaY = coordenadaY
        self.tiempo = tiempo
        self.idFrame = idFrame
        self.numberOfFrame = numberOfFrame

    def getIdPupila(self):
        return self.idPupila

    def getCoordenadaX(self):
        self.coordenadaX

    def getCoordenadaY(self):
        return self.coordenadaY

    def getTiempo(self):
        return self.tiempo

    def getIdFrame(self):
        return self.idFrame

    def getNumberOfFrame(self):
        return self.numberOfFrame

