
class Frame:
    def __init__(self, idFrame, numberOfFrame, rutaFrame, idVideo):
        self.idFrame = idFrame
        self.numberOfFrame = numberOfFrame
        self.rutaFrame = rutaFrame
        self.idVideo = idVideo


    def getIdFrame(self):
        return self.idFrame

    def getNumberOfFrame(self):
        return self.numberOfFrame

    def getRutaFrame(self):
        return self.rutaFrame

    def getIdVideo(self):
        return self.idVideo
