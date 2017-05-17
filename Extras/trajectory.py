import cv2
import numpy as np

center_points = []

def detecPupil(frame):
    global center_points

    gray = cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY)

    retval, thresholded = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    closed = cv2.erode(cv2.dilate(thresholded, kernel, iterations=1), kernel, iterations=1)

    contours, hierarchy = cv2.findContours(closed, cv2.cv.CV_RETR_LIST, cv2.cv.CV_CHAIN_APPROX_NONE)

    drawing = np.copy(frame)

    for contour in contours:
        area = cv2.contourArea(contour)
        bounding_box = cv2.boundingRect(contour)

        extend = area / (bounding_box[2] * bounding_box[3])

        # reject the contours with big extend
        #print 'Extend: ',extend
        if extend > 0.8:
            continue

        # calculate countour center and draw a dot there
        m = cv2.moments(contour)
        if m['m00'] != 0:
            center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
            cv2.circle(drawing, center, 3, (0, 255, 0), -1)
            center_points.append(center)
            print center
        # fit an ellipse around the contour and draw it into the image

        points = len(contour)
        if points < 5:
            continue

        ellipse = cv2.fitEllipse(contour)

        cv2.ellipse(drawing, box=ellipse, color=(0, 255, 0))


    return drawing

def drawCoordinate(frame):
#image = cv2.imread(frame)

    line_coordinates = []

    for point in center_points:
        cv2.circle(frame, tuple(point), 8, (0, 255, 0), -1)
        line_coordinates.append(tuple(point))
        print tuple(point)

    print line_coordinates

    for t in range(len(line_coordinates) - 1):
        print line_coordinates[t], line_coordinates[t + 1]
        cv2.line(frame, line_coordinates[t], line_coordinates[t + 1], (0, 255, 0), 2)

    return frame

def getCenterPoints():
    cv2.namedWindow('Pupil Detector', 1)
    cap = cv2.VideoCapture('output.avi')
    fourcc = cv2.cv.CV_FOURCC('i', 'Y', 'U', 'V')

    out = cv2.VideoWriter('output1.avi', fourcc, 20.0, (640, 480))

    # count = 0

    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:

            pupilImage = detecPupil(frame)

            # cv2.imwrite("frames/frame%d.jpg" % count, pupilImage)  # save frame as JPEG file
            # count += 1
            # print count

            out.write(pupilImage)

            cv2.imshow('Pupil Detector', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyWindow('Pupil Detector')
                break

        else:
            break

    cap.release()

    cv2.destroyAllWindows()

getCenterPoints()

cv2.namedWindow('Draw Coordinate', 1)
cap = cv2.VideoCapture('output.avi')
fourcc = cv2.cv.CV_FOURCC('i', 'Y', 'U', 'V')
out = cv2.VideoWriter('output2.avi', fourcc, 20.0, (640,480))

#count = 0

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:

        pupilImage= drawCoordinate(frame)

        #cv2.imwrite("frames/frame%d.jpg" % count, pupilImage)  # save frame as JPEG file
        #count += 1
        #print count

        out.write(pupilImage)

        cv2.imshow('Draw Coordinate',frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyWindow('Draw Coordinate')
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()

