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

from werkzeug.datastructures import FileStorage
import tempfile

#Videos dir -> folder with input video, frames folder and output video
#TODO make this a class
#Look into better ways of creating tempfiles, since doing it predictably yourself
#can lead to security vulnerabilities
#Why bash scripts so much slower when called from python?



#XXX
#with tempfile.TemporaryDirectory() as dirpath:
#XXX
class VideoProcessor:
  def __init__(self, input_file):
    #input_file is just the filename, no full path
    self.input_file = input_file
    self.filetype = input_file.split('.')[1]
    self.video_id = str(uuid.uuid4())
    self.fps = None

  @profile
  def setup(self):
    subprocess.check_output('sh create_directory.sh {0} {1} {2}'.format(self.video_id, self.input_file, self.filetype).split())

  @profile
  def altsetup(self):
    f = open('control_2.mp4', 'rb')
    #Simulates how file comes in via flask/werkzeug
    file = FileStorage(f)

    with tempfile.TemporaryDirectory() as dirpath:
      file.save(os.path.join(dirpath, 'input.mp4'))

    f.close()

  #Sampling options: frames per sec/minute/hour
  def get_frames(self):
    cap = cv2.VideoCapture('./videos/{0}/input.{1}'.format(self.video_id, self.filetype))
    #Potentially need to open here and check that the capture started
    #width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    self.fps = int(cap.get(cv2.CAP_PROP_FPS))
    seconds = num_frames / self.fps

    frames = [None] * num_frames
    for i in range(num_frames):
      frames[i] = cap.read()[1]

    #Release the capture
    cap.release()

    return frames

  def generate_frames(self):
    cap = cv2.VideoCapture('./videos/{0}/input.{1}'.format(self.video_id, self.filetype))
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for _ in range(num_frames):
      yield cap.read()[1]

    #Release the capture
    cap.release()

  def process_frames(self, frames):
    print('with pool')
    with Pool(4) as pool: #Could also use cv2.getNumberOfCPUs()
      pool.map(self.modify_frame, enumerate(frames)) #Processes

  def process_frames_iterative(self, frames):
    print('iterative')
    for i, frame in enumerate(frames):
      self.modify_frame((i, frame))

  def modify_frame(self, _frame):
    num, frame = _frame
    frame = self.apply_changes(frame)
    cv2.imwrite('./videos/%s/frames/frame%04d.bmp' % (self.video_id, num), frame)

  def apply_changes(self, frame):
    return cv2.flip(frame, 0)

  def gen_process_video(self):
    #.bmp has no compression, so all image files will be the same size, but writing is faster
    #.png has compression so file sizes vary, but takes longer to write
    frames = self.generate_frames()
    self.process_frames_iterative(frames)
    #self.process_frames(frames)

    return 10

  def cleanup(self):
    output_cmd = 'sh build_output.sh {0} {1} {2}'.format(self.video_id, self.fps, self.filetype)
    subprocess.check_output(output_cmd.split())

@profile
def main():
  vp = VideoProcessor('control_2.mp4')
  vp.setup()
  vp.altsetup()
  #vp.gen_process_video()
  #vp.cleanup()


if __name__ == '__main__':
  main()

#Seems like opencv faster at reading frames than using ffmpeg to split into frames (disk time?)
#Seems like ffmpeg faster at building a video out of frames than opencv writing
#Could try creating images out of frames and stitching them together using 
#ffmpeg -framerate 10 -start_number 0 -i frame%d.png -vcodec mpeg4 test.mp4
#Can also append frames to video, would be interesting to test
