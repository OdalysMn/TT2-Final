
class Frame:
    def __init__(self, idFrame, numberOfFrame, rutaFrame, idVideo):
        self.idFrame = idFrame
        self.numberOfFrame = numberOfFrame
        self.rutaFrame = rutaFrame
        self.idVideo = idVideo

    def strFrame(self):
        return "%s %s %s %s" % (self.idFrame,self.numberOfFrame,self.rutaFrame,self.idVideo)
