import cv2
import numpy as np
import math

pupil_coordenates = []
fileResults = open('pupila.txt', 'wb')
#transform_coordenates = []
#totalFrames = 0

def getFrames(videoFileRoute, framesFileRoute):
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

def euclidianDistance(a,b):
    lstA = list(a)
    lstB = list(b)

    x1 = lstA[0]
    y1 = lstA[1]

    x2 = lstB[0]
    y2 = lstB[1]

    d = math.sqrt(((math.pow((x2-x1),2))+( math.pow((y2-y1),2))))

    #print "euclidian distance: ",d

    return d

def escalarCoodinatesPupil(c):

    lst = list(c)
    lst[0] += 200
    lst[1] += 140
    newC = tuple(lst)

    return newC

def escalarCoordinatesTrayectori(t):

    lst = list(t)

    #lst[0] = int(round(lst[0] * 3.2, 0))
    #lst[1] = int(round(lst[1] * 3.42857142, 0))

    lst[0] = int(round(lst[0] * 2.666666, 0))
    lst[1] = int(round(lst[1] * 3, 0))

    #lst[0] = int(round(lst[0] * 1.454545, 0))
    #lst[1] = int(round(lst[1] * 1.411764, 0))

    newT = tuple(lst)

    return newT


def detecPupil(name,numberOfFrame):
    centers = []
    global pupil_coordenates
    global fileResults

    image = cv2.imread(name)
    #frame = image
    frame = cv2.flip(image, 1)

    cv2.imshow('invert', frame)

    crop_img = frame[140:300, 200:440]
    cv2.imshow('cropped', crop_img)

    gray = cv2.cvtColor(crop_img, cv2.cv.CV_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    #gray = (255-gray)
    cv2.imshow('gray', gray)

    retval, thresholded = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)

    cv2.imshow('thresholded', thresholded)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    closed = cv2.erode(cv2.dilate(thresholded, kernel, iterations=1), kernel, iterations=1)
    contours, hierarchy = cv2.findContours(closed , cv2.cv.CV_RETR_LIST, cv2.cv.CV_CHAIN_APPROX_NONE)

    drawing = np.copy(frame)
    drawing_crop = np.copy(crop_img)

    for contour in contours:
        contour = cv2.convexHull(contour)

        area = cv2.contourArea(contour)

        #if area < 100:
         #   continue

        bounding_box = cv2.boundingRect(contour)

        extend = area / (bounding_box[2] * bounding_box[3])

        #print "extend: ",extend

        # reject the contours with big extend
        if extend > 0.9:
           continue

        # calculate countour center and draw a dot there
        m = cv2.moments(contour)

        if m['m00'] != 0:
            center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
            #center = escalarCoodinatesPupil(center)
            centers.append(center)
            #print "center: ",center


    #print "number of frame: ",numberOfFrame

    if len(centers) > 1:
        distances = []
        if numberOfFrame > 0:
            for c in centers:
                dist = euclidianDistance(pupil_coordenates[numberOfFrame-1],c)
                distances.append(dist)

            #print "distances: ",distances
            min_dist = min(distances)
            #print "min_value: ",min_dist

            for d in distances:
                if d == min_dist:
                    index_min_dist = distances.index(d)

            cv2.circle(drawing_crop, centers[index_min_dist], 4, 255, 2)
            #cv2.circle(drawing, centers[index_min_dist], 4, 255, 2)'
            pupil_coordenates.append(centers[index_min_dist])
        else:
            for c in centers:
                dist = euclidianDistance((120, 80), c)
                distances.append(dist)

            # print "distances: ",distances
            min_dist = min(distances)
            # print "min_value: ",min_dist

            for d in distances:
                if d == min_dist:
                    index_min_dist = distances.index(d)

            cv2.circle(drawing_crop, centers[index_min_dist], 4, 255, 2)
            # cv2.circle(drawing, centers[index_min_dist], 4, 255, 2)'
            pupil_coordenates.append(centers[index_min_dist])

        line = str(numberOfFrame)+' ,frame: '+name+' ,pupila:SI'+'\n'

    elif len(centers) == 0:
        if numberOfFrame > 0:
            cv2.circle(drawing_crop, pupil_coordenates[numberOfFrame-1], 4, 255, 2)
            #cv2.circle(drawing, pupil_coordenates[numberOfFrame-1], 4, 255, 2)
            pupil_coordenates.append(pupil_coordenates[numberOfFrame-1])
        else:
            cv2.circle(drawing_crop, (120, 80), 4, 255, 2)
            # cv2.circle(drawing, pupil_coordenates[numberOfFrame-1], 4, 255, 2)
            pupil_coordenates.append((120, 80))

        line = str(numberOfFrame) + ' ,frame: ' + name + ' ,pupila:NO' + '\n'

    else:
        cv2.circle(drawing_crop, centers[len(centers)-1], 4, 255, 2)
        #cv2.circle(drawing, centers[len(centers)-1], 4, 255, 2)
        pupil_coordenates.append(centers[len(centers)-1])
        line = str(numberOfFrame) + ' ,frame: ' + name + ' ,pupila:SI' + '\n'

    fileResults.write(line)

    print 'centers: ', centers

    drawing[140:300, 200:440] = drawing_crop
    #cv2.circle(drawing_crop, (0,0), 16, (0,255,0), -1)
    #cv2.circle(drawing_crop, (200, 140), 16, (0,255,0), -1)
    #cv2.circle(drawing_crop, (240, 200), 16, (0,255,0), -1)
    cv2.rectangle(drawing, (200, 140), (440, 300), (255, 0, 0), 2)
    cv2.imshow('drawing', drawing)
    cv2.imshow('drawing_crop', drawing_crop)

    return drawing

def drawCoordinate(nombre_frame, points):
    image = cv2.imread(nombre_frame)

    line_coordinates = []

    for point in points:
        cv2.circle(image, tuple(point), 4, 255, -1)
        #font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(image, str(points.index(point)), tuple(point), font, 1, (255, 255, 255), 1, 255)
        line_coordinates.append(tuple(point))

    for t in range(len(line_coordinates) - 1):

        cv2.line(image, line_coordinates[t], line_coordinates[t + 1], 255, 1)

    return image


videoToProcess = 'ojo.avi'
framesFileRoute = 'frames/'

totalFrames = getFrames(videoToProcess,framesFileRoute)

print "total Frames: ", totalFrames

cv2.namedWindow('Pupil Detector', 1)
fourcc = cv2.cv.CV_FOURCC('i', 'Y', 'U', 'V')
out = cv2.VideoWriter('NoPupila.avi', fourcc, 20.0, (640,480))
numFrame = 0

while(numFrame < totalFrames):

    print "number of Frame",numFrame

    pupilImage= detecPupil(framesFileRoute+str(numFrame)+'.jpg',numFrame)

    cv2.imwrite("frames4/%d.jpg" % numFrame, pupilImage)  # save frame as JPEG file
    numFrame += 1


    out.write(pupilImage)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyWindow('Pupil Detector')
        break

fileResults.close()
print 'pupil_coordenates: ', pupil_coordenates
print 'Pupil Detector Finish'

transform_coordenates = []
for p in pupil_coordenates:
    transform_coordenates.append(escalarCoordinatesTrayectori(p))

print "transform_coordenates: ", transform_coordenates


videoToProcess2 = 'escena.avi'

numFrame2 = 0
out2 = cv2.VideoWriter('trayectoria.avi', fourcc, 20.0, (640, 480))
rutaFramesLeer = 'frames2/'

totalFrames2 = getFrames(videoToProcess2,rutaFramesLeer)


while numFrame2 < totalFrames2:

    points = []
    count = 0
    print numFrame2
    while count < numFrame2:

        points.append(transform_coordenates[count])
        count = count + 1

    trayectImage = drawCoordinate(rutaFramesLeer + str(numFrame2) + '.jpg', points)
    cv2.imwrite('frames3/' + "%d.jpg" % numFrame2, trayectImage)
    out2.write(trayectImage)

    numFrame2 = numFrame2 + 1
