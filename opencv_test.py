import numpy as np
import cv2
import os
from threading import Thread
from queue import Queue
import time
import uuid


#from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool as ThreadPool

#Videos dir -> folder with input video, frames folder and output video

def process_frame(frame):
  #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  frame = cv2.flip(frame, 0)
  return frame

#@profile
def process_video(input_file):
  #input_file is just the filename, no full path

  input_filename, input_filetype = input_file.split('.')
  video_id = str(uuid.uuid4())

  #Rename video and move it into a temporary working directory
  tmp_dir = './videos/' + video_id
  os.mkdir(tmp_dir)
  os.mkdir(tmp_dir + '/frames')
  tmp_filename = tmp_dir + '/' + video_id + '.input.' + input_filetype
  os.system(' '.join(['cp', './' + input_file, tmp_filename]))


  cap = cv2.VideoCapture(tmp_filename)
  #Potentially need to open here and check that the capture started
  width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  fps = int(cap.get(cv2.CAP_PROP_FPS))

  #Both are MPEG4 but with different codecs
  #Control2 -> MPEG-4
  #Output -> H.264

  print(num_frames, fps, num_frames / fps) #seconds
  print(width, height)

  fourcc = cv2.VideoWriter_fourcc(*'MP4V')

  output_filename = tmp_dir + '/' + video_id + '.output.' + input_filetype
  #out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

  frame_name = tmp_dir + '/frames/frame%d.png' #Need to account for high frame counts?
  '''
  for i in range(num_frames):
      # Capture frame-by-frame
      success, frame = cap.read()

      if not success:
        print("ran out of frames")
        break

      # Our operations on the frame come here
      frame = process_frame(frame)

      #out.write(frame)
      cv2.imwrite(frame_name % i, frame)
      #Has quality difference 40.7 mb -> 5.8 mb
      #cv2.imshow('Frame', frame)

      # Display the resulting frame
      #cv2.imshow('frame', frame)
      #if cv2.waitKey(1) & 0xFF == ord('q'):
          #break
  '''
  frames = []
  for i in range(num_frames):
    _, frame = cap.read()
    frames.append((i, frame))

  pool = ThreadPool(4)
  #2->15
  #4->12
  #6->13
  #8->12.5
  def tmpfunc(_frame):
    i, frame = _frame
    frame = process_frame(frame)
    cv2.imwrite(frame_name % i, frame)

  #pool.map(tmpfunc, frames) #threads
  pool.map(tmpfunc_top, frames) #Processes
  pool.close()
  pool.join()

  # When everything done, release the capture
  cap.release()
  #out.release()
  cv2.destroyAllWindows()


  #Build output video
  output_cmd = 'ffmpeg -framerate {0} -start_number 0 -i {1} -vcodec mpeg4 {2}'.format(fps, frame_name, output_filename)
  print(output_cmd)
  #os.system(output_cmd)

def tmpfunc_top(_frame):
  frame_name = './tmp/frames/frame%d.png' #Need to account for high frame counts?
  i, frame = _frame
  frame = process_frame(frame)
  cv2.imwrite(frame_name % i, frame)


if __name__ == '__main__':
  process_video('control_2.mp4')
#Seems like opencv faster at reading frames than using ffmpeg to split into frames (disk time?)
#Seems like ffmpeg faster at building a video out of frames than opencv writing
#Could try creating images out of frames and stitching them together using 
#ffmpeg -framerate 10 -start_number 0 -i frame%d.png -vcodec mpeg4 test.mp4
#Can also append frames to video, would be interesting to test
