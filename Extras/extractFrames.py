import cv2

import numpy as np
import cv2

cap = cv2.VideoCapture('ojo1.avi')
count = 0

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret==True:

        # write the frame
        cv2.imwrite("frames/frame%d.jpg" % count, frame)  # save frame as JPEG file
        count += 1
        print count

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()






