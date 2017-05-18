import os

class Sistema:

    def createDirectory(self,path):

        try:
            os.makedirs(path)
        except OSError:
            if not os.path.isdir(path):
                raise


