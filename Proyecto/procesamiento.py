import cv2
import numpy as np
import math

class Procesamiento:
    def __init__(self):
        self.pupil_coordenates = []
        self.tray_coordenates = []

    def getFrames(self,videoFileRoute, framesFileRoute):
        cap = cv2.VideoCapture(videoFileRoute)
        totalFrames = 0

        while (cap.isOpened()):

            ret, frame = cap.read()
            if ret == True:

                # write the frame
                cv2.imwrite(framesFileRoute + "%d.jpg" % totalFrames, frame)  # save frame as JPEG file
                totalFrames += 1
                print totalFrames

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        # Release everything if job is finished
        cap.release()
        return totalFrames

    def euclidianDistance(self,a,b):
        lstA = list(a)
        lstB = list(b)

        x1 = lstA[0]
        y1 = lstA[1]

        x2 = lstB[0]
        y2 = lstB[1]

        d = math.sqrt(((math.pow((x2 - x1), 2)) + (math.pow((y2 - y1), 2))))

        # print "euclidian distance: ",d

        return d

    def escalarCoodinatesPupil(self,c):
        lst = list(c)
        lst[0] += 200
        lst[1] += 140
        newC = tuple(lst)

        return newC

    def escalarCoordinatesTrayectori(self,t):
        lst = list(t)

        lst[0] = int(round(lst[0] * 3.2, 0))
        lst[1] = int(round(lst[1] * 3.42857142, 0))

        newT = tuple(lst)

        return newT

    def detecPupil(self,name,numberOfFrame):
        centers = []

        image = cv2.imread(name)
        frame = cv2.flip(image, 1)

        crop_img = frame[140:340, 200:440]
        #cv2.imshow('cropped', crop_img)

        gray = cv2.cvtColor(crop_img, cv2.cv.CV_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        # gray = (255-gray)
        #cv2.imshow('gray', gray)

        retval, thresholded = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)

        #cv2.imshow('thresholded', thresholded)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        closed = cv2.erode(cv2.dilate(thresholded, kernel, iterations=1), kernel, iterations=1)
        contours, hierarchy = cv2.findContours(closed, cv2.cv.CV_RETR_LIST, cv2.cv.CV_CHAIN_APPROX_NONE)

        drawing = np.copy(frame)
        drawing_crop = np.copy(crop_img)

        for contour in contours:
            contour = cv2.convexHull(contour)

            area = cv2.contourArea(contour)

            if area < 400:
                continue

            bounding_box = cv2.boundingRect(contour)

            extend = area / (bounding_box[2] * bounding_box[3])

            # reject the contours with big extend
            if extend > 0.9:
                continue

            # calculate countour center and draw a dot there
            m = cv2.moments(contour)

            if m['m00'] != 0:
                center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                # center = escalarCoodinatesPupil(center)
                centers.append(center)
                print "center: ", center

        # print "number of frame: ",numberOfFrame

        if len(centers) > 1:
            distances = []
            if numberOfFrame > 0:
                for c in centers:
                    dist = self.euclidianDistance(self.pupil_coordenates[numberOfFrame - 1], c)
                    distances.append(dist)

                # print "distances: ",distances
                min_dist = min(distances)
                # print "min_value: ",min_dist

                for d in distances:
                    if d == min_dist:
                        index_min_dist = distances.index(d)

                cv2.circle(drawing_crop, centers[index_min_dist], 4, 255, 2)
                # cv2.circle(drawing, centers[index_min_dist], 4, 255, 2)'
                self.pupil_coordenates.append(centers[index_min_dist])

        elif len(centers) == 0:
            if numberOfFrame > 0:
                cv2.circle(drawing_crop, self.pupil_coordenates[numberOfFrame - 1], 4, 255, 2)
                # cv2.circle(drawing, pupil_coordenates[numberOfFrame-1], 4, 255, 2)
                self.pupil_coordenates.append(self.pupil_coordenates[numberOfFrame - 1])

        else:
            cv2.circle(drawing_crop, centers[len(centers) - 1], 4, 255, 2)
            # cv2.circle(drawing, centers[len(centers)-1], 4, 255, 2)
            self.pupil_coordenates.append(centers[len(centers) - 1])

        print 'centers: ', centers

        drawing[140:340, 200:440] = drawing_crop
        #cv2.imshow('drawing', drawing)
        #cv2.imshow('drawing_crop', drawing_crop)

        return drawing

    def drawCoordinate(self,nombre_frame, points):
        image = cv2.imread(nombre_frame)

        line_coordinates = []

        for point in points:
            cv2.circle(image, tuple(point), 4, 255, 2)
            # font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(image, str(points.index(point)), tuple(point), font, 1, (255, 255, 255), 1, 255)
            # line_coordinates.append(tuple(point))

        # for t in range(len(line_coordinates) - 1):

        #    cv2.line(image, line_coordinates[t], line_coordinates[t + 1], 255, 1)

        return image

    def marcarPupilas(self,rutaVideoProcesar,rutaVideoGuardar, rutaFramesGuardarAntes, rutaFramesGuardar):
        fourcc = cv2.cv.CV_FOURCC('i', 'Y', 'U', 'V')
        self.outPupila = cv2.VideoWriter(rutaVideoGuardar, fourcc, 20.0, (640, 480))
        numFrame = 0
        totalFrames = self.getFrames(rutaVideoProcesar,rutaFramesGuardarAntes)

        while (numFrame < totalFrames):
            name = rutaFramesGuardarAntes + str(numFrame) + '.jpg'

            pupilImage = self.detecPupil(name,numFrame)

            cv2.imwrite(rutaFramesGuardar + "%d.jpg" % numFrame, pupilImage)  # save frame as JPEG file
            numFrame += 1
            print numFrame

            self.outPupila.write(pupilImage)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.outPupila = None

    def marcarTrayectoria(self, rutaVideoProcesar,rutaVideoGuardar, rutaFramesGuardarAntes, rutaFramesGuardar):
        fourcc = cv2.cv.CV_FOURCC('i', 'Y', 'U', 'V')
        self.outTray = cv2.VideoWriter(rutaVideoGuardar, fourcc, 20.0, (640, 480))
        numFrame = 0
        totalFrames = self.getFrames(rutaVideoProcesar,rutaFramesGuardarAntes)
        for p in self.pupil_coordenates:
            self.tray_coordenates.append(self.escalarCoordinatesTrayectori(p))

        while numFrame < totalFrames:

            points = []
            count = 0
            print numFrame
            while count < numFrame:
                # print "Tupla: ", self.center_points[count2]

                points.append(self.tray_coordenates[count])
                count = count + 1

            pupilImage = self.drawCoordinate(rutaFramesGuardarAntes + str(numFrame) + '.jpg', points)
            cv2.imwrite(rutaFramesGuardar + "%d.jpg" % numFrame, pupilImage)
            self.outTray.write(pupilImage)

            numFrame = numFrame + 1

        self.outTray = None