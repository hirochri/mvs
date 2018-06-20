import numpy as np
import cv2
import os
from threading import Thread
from queue import Queue
import time
import uuid
import subprocess
import shutil

from multiprocessing import Pool
from functools import partial

#Videos dir -> folder with input video, frames folder and output video
#TODO make this a class
#Look into better ways of creating tempfiles, since doing it predictably yourself
#can lead to security vulnerabilities
#Why bash scripts so much slower when called from python?

def create_directory(input_file):
  filetype = input_file.split('.')[1]
  video_id = str(uuid.uuid4())

  subprocess.check_output('sh create_directory.sh {0} {1} {2}'.format(video_id, input_file, filetype), shell=True)

  #Returns video id and input and output file names
  return video_id, filetype

def get_frames(video_id, filetype):
  cap = cv2.VideoCapture('./videos/{0}/input.{1}'.format(video_id, filetype))
  #Potentially need to open here and check that the capture started
  width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  fps = int(cap.get(cv2.CAP_PROP_FPS))
  seconds = num_frames / fps

  frames = [None] * num_frames
  for i in range(num_frames):
    frames[i] = cap.read()[1]

  #Release the capture
  cap.release()
  cv2.destroyAllWindows()

  return frames, fps

def process_frames(video_id, frames):
  with Pool(4) as pool:
    modify_frame = partial(_modify_frame, video_id=video_id)
    pool.map(modify_frame, enumerate(frames)) #Processes

def _modify_frame(_frame, video_id):
  num, frame = _frame
  frame = apply_changes(frame)
  cv2.imwrite('./videos/%s/frames/frame%04d.bmp' % (video_id, num), frame)

def apply_changes(frame):
  return cv2.flip(frame, 0)

def process_video(input_file):
  #input_file is just the filename, no full path
  video_id, filetype = create_directory(input_file)

  frames, fps = get_frames(video_id, filetype)
  #.bmp has no compression, so all image files will be the same size, but writing is faster
  #.png has compression so file sizes vary, but takes longer to write

  process_frames(video_id, frames)

  output_cmd = 'sh build_output.sh {0} {1} {2}'.format(video_id, fps, filetype)
  subprocess.check_output(output_cmd, shell=True)

if __name__ == '__main__':
  process_video('control_2.mp4')
#Seems like opencv faster at reading frames than using ffmpeg to split into frames (disk time?)
#Seems like ffmpeg faster at building a video out of frames than opencv writing
#Could try creating images out of frames and stitching them together using 
#ffmpeg -framerate 10 -start_number 0 -i frame%d.png -vcodec mpeg4 test.mp4
#Can also append frames to video, would be interesting to test
