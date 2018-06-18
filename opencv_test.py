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



#Could be interesting to use python library: 'tempfile', not sure about performance though
def create_directory(input_file):
  filetype = input_file.split('.')[1]
  video_id = str(uuid.uuid4())

  #Rename video and move it into a temporary working directory
  video_dir = './videos/' + video_id
  os.mkdir(video_dir)
  os.mkdir(video_dir + '/frames')
  input_filename = video_dir + '/input.' + filetype
  os.system(' '.join(['cp', './' + input_file, input_filename]))
  #Returns video id and input and output file names
  output_filename = video_dir + '/output.' + filetype
  return video_id, input_filename, output_filename

def remove_directory(video_id):
  pass

def get_frames(input_filename):
  cap = cv2.VideoCapture(input_filename)
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

def process_frames(frame_name, frames):
  modify_frame= partial(_modify_frame, frame_name=frame_name)

  pool = Pool(4)
  pool.map(modify_frame, enumerate(frames)) #Processes
  pool.close()
  pool.join()

def _modify_frame(_frame, frame_name):
  num, frame = _frame
  frame = apply_changes(frame)
  cv2.imwrite(frame_name % num, frame)

def apply_changes(frame):
  frame = cv2.flip(frame, 0)
  return frame

def process_video(input_file):
  #input_file is just the filename, no full path
  video_id, input_filename, output_filename = create_directory(input_file)

  frames, fps = get_frames(input_filename)
  frame_name = './videos/'+ video_id + '/frames/frame%04d.png' #Need to account for high frame counts?

  process_frames(frame_name, frames)

  #Build output video
  output_cmd = 'ffmpeg -framerate {0} -start_number 0 -i {1} -vcodec mpeg4 {2}'.format(fps, frame_name, output_filename)
  subprocess.Popen(output_cmd.split()).wait()

  #shutil.rmtree('./videos/' + video_id + '/frames')

#Hacky, can be improved later, assumes 4+ frames
def four_chunks(lst):
  m = len(lst) // 2
  x, y = lst[:m], lst[m:]
  mx, my = len(x) // 2, len(y) // 2
  return [x[:mx], x[mx:], y[:my], y[my:]]
#mylist.txt has lines like: file video.mp4
#ffmpeg -f concat -i mylist.txt -c copy output.mp4


if __name__ == '__main__':
  process_video('control_2.mp4')
#Seems like opencv faster at reading frames than using ffmpeg to split into frames (disk time?)
#Seems like ffmpeg faster at building a video out of frames than opencv writing
#Could try creating images out of frames and stitching them together using 
#ffmpeg -framerate 10 -start_number 0 -i frame%d.png -vcodec mpeg4 test.mp4
#Can also append frames to video, would be interesting to test
