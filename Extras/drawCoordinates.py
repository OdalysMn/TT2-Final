import cv2
import numpy as np

def drawCoordinate(nombre_frame, points):
    image = cv2.imread(nombre_frame)

    line_coordinates = []

    for point in points:
        cv2.circle(image, tuple(point), 18, 255, -1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, str(points.index(point)), tuple(point), font, 1, (255, 255, 255), 1, 255)
        line_coordinates.append(tuple(point))
        #print tuple(point)

    #print line_coordinates

    for t in range(len(line_coordinates) - 1):
    #    print line_coordinates[t], line_coordinates[t + 1]
        cv2.line(image, line_coordinates[t], line_coordinates[t + 1], 255, 1)


    return image


center_points = [
    [35, 103], [336, 75], [303, 57], [271, 51], [277, 3], [214, 3], [24, 113], [331, 74],[266, 55],[272, 5],
    [209, 4], [325, 81], [262, 58], [21, 119], [330, 79], [296, 64], [264, 57], [262, 87], [21, 116], [333, 78],
    [268, 55], [117, 29], [267, 86], [244, 115], [235, 142], [233, 134], [236, 130], [236, 129], [234, 127], [233, 125],
    [232, 125], [233, 129], [239, 128], [240, 104], [161, 114], [26, 105], [206, 2], [161, 112], [205, 2], [157, 112],
    [25, 106], [257, 47], [200, 2], [155, 110], [22, 104], [196, 2], [153, 110], [194, 2], [155, 112], [23, 103]
    ]

count = 0
fourcc = cv2.cv.CV_FOURCC('i', 'Y', 'U', 'V')
out = cv2.VideoWriter('output4.avi', fourcc, 20.0, (640,480))

while count < 50:

    points = []
    count2 = 0
    print count
    while count2 < count:
        points.append(center_points[count2])
        count2 = count2 + 1


    pupilImage = drawCoordinate('vista/framesEscena/frame'+str(count)+'.jpg',points)
    cv2.imwrite("frames4/frametray%d.jpg" % count, pupilImage)
    out.write(pupilImage)

    count = count +1

#while(cap.isOpened()):
 #   ret, frame = cap.read()
  #  if ret==True:

   #     for point in center_points:
    #        pupilImage = drawCoordinate(frame,point)

            #cv2.imwrite("frames/frame%d.jpg" % count, pupilImage)  # save frame as JPEG file
            #count += 1
            #print count

     #       out.write(pupilImage)

      #      cv2.imshow('Draw Coordinate',frame)


       #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #        cv2.destroyWindow('Draw Coordinate')
         #       break

    #else:
     #   break

#cap.release()

#cv2.destroyAllWindows()



