import numpy as np
import cv2

cap = cv2.VideoCapture('./control_2.mp4')
#Potentially need to open here and check that the capture started
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
f = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

#Both are MPEG4 but with different codecs
#Control2 -> MPEG-4
#Output -> H.264

print(f, fps, f / fps) #seconds

exit()
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('./output.mp4', fourcc, fps, (w, h))

while(True): #loop over frames?
    # Capture frame-by-frame
    success, frame = cap.read()

    if not success:
      break

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    frame = cv2.flip(frame, 0)
    out.write(frame) #Make sure file doesn't already exist

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
