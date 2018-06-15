import numpy as np
import cv2
import os
from threading import Thread
from queue import Queue
import time

#@profile
def main():
  cap = cv2.VideoCapture('./control_2.mp4')
  #Potentially need to open here and check that the capture started
  width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  fps = int(cap.get(cv2.CAP_PROP_FPS))

  #Both are MPEG4 but with different codecs
  #Control2 -> MPEG-4
  #Output -> H.264

  print(num_frames, fps, num_frames / fps) #seconds

  fourcc = cv2.VideoWriter_fourcc(*'MP4V')

  #Make sure file doesn't already exist
  if os.path.isfile('./output.mp4'):
    os.remove('./output.mp4')

  out = cv2.VideoWriter('./output.mp4', fourcc, fps, (width, height))

  for i in range(num_frames):
      # Capture frame-by-frame
      success, frame = cap.read()

      if not success:
        print("ran out of frames")
        break

      # Our operations on the frame come here
      #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


      #frame = cv2.flip(frame, 0)
      #out.write(frame)
      cv2.imwrite("tmp/frame%d.png" % i, frame) #Slight quality difference
      #cv2.imshow('Frame', frame)

      # Display the resulting frame
      #cv2.imshow('frame', frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break

  # When everything done, release the capture
  cap.release()
  out.release()
  cv2.destroyAllWindows()

class ThreadedParse:
  def __init__(self):
    self.cap = cv2.VideoCapture('./control_2.mp4')
    self.stopped = False

    self.Q = Queue(maxsize=50)

  def start(self):
    t = Thread(target=self.update, args=())
    t.daemon = True
    t.start()
    return self

  def update(self):
    while True:
      if self.stopped:
        return

      if not self.Q.full():
        success, frame = self.cap.read()

        if not success:
          self.stop()
          return

        self.Q.put(frame)

  def read(self):
    return self.Q.get()

  def more(self):
    return self.Q.qsize() > 0

  def stop(self):
    self.stopped = True


#@profile
def threaded_main():
  tp = ThreadedParse().start()

  width = int(tp.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(tp.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  #num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  fps = int(tp.cap.get(cv2.CAP_PROP_FPS))
  fourcc = cv2.VideoWriter_fourcc(*'MP4V')

  if os.path.isfile('./output.mp4'):
    os.remove('./output.mp4')
  out = cv2.VideoWriter('./output.mp4', fourcc, fps, (width, height))

  time.sleep(1) #for Queue to fill

  count = 0
  while tp.more():
    frame = tp.read()
    frame = cv2.flip(frame, 0)
    cv2.imwrite("tmp/frame%d.png" % count, frame)
    #cv2.imshow('Frame', frame)
    #out.write(frame)
    #cv2.waitKey(1) #Not needed without GUI
    count += 1

  tp.stop()
  tp.cap.release()
  out.release()
  cv2.destroyAllWindows()

#threaded_main()
main()


#Could try creating images out of frames and stitching them together using 
#ffmpeg -framerate 10 -start_number 0 -i frame%d.png -vcodec mpeg5 test.mp4
