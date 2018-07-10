import numpy as np
import cv2
import os
import time
from werkzeug.datastructures import FileStorage
import tempfile
from subprocess import Popen, PIPE
from functools import reduce

class VideoProcessor:
  def __init__(self, funcs):
    self.funcs = funcs
    self.generated_data = {}

  def test_run(self):
    test_file = 'control_2.mp4'
    f = open(test_file, 'rb')
    #Simulates how file comes in via flask/werkzeug
    file = FileStorage(f)

    ###################
    #self.process_video(file, 10, 0)
    self.process_video(file, 5, 0, 5)
    ###################

    f.close()

  def get_sampling_fps(self, sampling_rate, sampling_time):
    #sampling_time = 0 for seconds, 1 for minutes, 2 for hours

    #Convert to fps
    if sampling_time > 0:
      sampling_fps = sampling_rate / (60 ** sampling_time)
    else:
      sampling_fps = sampling_rate

    return sampling_fps

  def get_sampling_modulo(self, source_fps, sampling_fps):
    print('Original video: {0} fps'.format(source_fps))
    print('Sampling at {0} fps'.format(sampling_fps))
    modulo = source_fps / sampling_fps 
    #Deal with gross numbers
    if modulo % 1 != 0: 
      print('Modulo {0} wont work, Sampling fps adjusted to {1}'.format(modulo, source_fps / int(modulo)))

    #XXX Floors gross numbers for now
    modulo = int(modulo)
    print('Using modulo {0} to sample frames'.format(modulo))

    return modulo

  def create_frame_generator(self, filename, sampling_rate, sampling_time):
    cap = cv2.VideoCapture(filename)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dimensions = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    sampling_fps = self.get_sampling_fps(sampling_rate, sampling_time)
    sampling_modulo = self.get_sampling_modulo(fps, sampling_fps)

    def generator():
      for num in range(num_frames):
        #Generate data based on all frames

        frame = cap.read()[1]

        if num % sampling_modulo == 0:
          yield (num, frame)
        #Frame number, frame
        #Can calculate timestamp from frame number and fps

      #Release the capture
      cap.release()

    return dimensions, generator

  def process_video(self, file, sampling_rate, sampling_time, output_fps=10):
    with tempfile.TemporaryDirectory() as dirpath:
      filename = os.path.join(dirpath, 'input.mp4')
      file.save(filename)
      #TODO save original input to same spot as output

      frame_dimensions, frame_generator = self.create_frame_generator(filename, sampling_rate, sampling_time)

      cmd = [
          'ffmpeg', '-y', #Overwrite input files
          '-f', 'rawvideo', 
          '-vcodec', 'rawvideo',
          '-s', '{0}x{1}'.format(*frame_dimensions),
          '-pix_fmt', 'rgb24',
          '-r', str(output_fps),
          '-i', '-',
          '-an', #Expect no audio
          '-vcodec', 'mpeg4',
          'hirotest.mp4'
      ]

      p = Popen(cmd, stdin=PIPE)

      for num, frame in frame_generator():
        print('NUM', num)
        #Generate data for sampled frame

        #Apply functions to sampled frame
        frame = self.apply_functions(frame)

        #Frame composition stuff?

        p.stdin.write(frame.tostring())

      #XXX read up on how Popen knows when stdin ends

  def apply_functions(self, frame):
    return reduce(lambda res, func: func(res), self.funcs, frame)

def flip_frame(frame):
  return cv2.flip(frame, 0)

if __name__ == '__main__':
  vp = VideoProcessor([flip_frame, flip_frame])
  vp.test_run()
