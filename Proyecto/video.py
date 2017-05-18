
class Video:
    def __init__(self, idVideo, rutaVideo, rutaFrames, tipoVideo, idPrueba):
        self.idVideo = idVideo
        self.rutaVideo = rutaVideo
        self.rutaFrames = rutaFrames
        self.tipoVideo = tipoVideo
        self.idPrueba = idPrueba

    def getIdVideo(self):
        return self.idVideo

    def getRutaVideo(self):
        return self.rutaVideo

    def getRutaFrames(self):
        return self.rutaFrames

    def getTipoVideo(self):
        return self.tipoVideo

    def getIdPrueba(self):
        return self.idPrueba