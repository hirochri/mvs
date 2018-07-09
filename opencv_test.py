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
    #test_file = 'city.mp4'
    f = open(test_file, 'rb')
    #Simulates how file comes in via flask/werkzeug
    file = FileStorage(f)

    ###################
    self.process_video(file)
    ###################

    f.close()





  def create_frame_generator(self, filename):
    cap = cv2.VideoCapture(filename)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dimensions = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    def generator():
      for num in range(num_frames):
        #Generate data based on all frames

        #if frame supposed to be sampled
        yield (num, cap.read()[1])
        #Frame number, frame
        #Can calculate timestamp from frame number and fps

      #Release the capture
      cap.release()

    return fps, dimensions, generator

  def process_video(self, file):
    with tempfile.TemporaryDirectory() as dirpath:
      filename = os.path.join(dirpath, 'input.mp4')
      file.save(filename)

      source_fps, frame_dimensions, frame_generator = self.create_frame_generator(filename)
      print(source_fps)

      fps = 10
      cmd = [
          'ffmpeg', '-y', #Overwrite input files
          '-f', 'rawvideo', 
          '-vcodec', 'rawvideo',
          '-s', '{0}x{1}'.format(*frame_dimensions),
          '-pix_fmt', 'rgb24',
          '-r', str(fps),
          '-i', '-',
          '-an', #Expect no audio
          '-vcodec', 'mpeg4',
          'hirotest.mp4'
      ]
      #scmd = 'ffmpeg -y -f rawvideo -vcodec rawvideo -s {0}x{1} -pix_fmt rgb24 -r {2} -i - -an -vcodec mpeg4 hirotest.mp4'.format(self.w,self.h, self.fps)
      #cmd = scmd.split()
      p = Popen(cmd, stdin=PIPE)

      for num, frame in frame_generator():
        print('NUM', num)
        #Generate data for frame

        #Apply functions to frame
        frame = self.apply_functions(frame)

        #Frame composition stuff?

        p.stdin.write(frame.tostring())

      #XXX read up on how Popen knows when stdin ends

  def apply_functions(self, frame):
    return reduce(lambda res, func: func(res), self.funcs, frame)

def flip_frame(frame):
  return cv2.flip(frame, 0)

'''
Incoming sampling fps cannot be higher than original video fps
Output sampling should also be selectable

x fps videos -> sample 1-x fps, 1-(x*60) fpm, 1-(x*60*60) fph

down = fps * 60 * 60
1/2 fps = 1 frame per 2 seconds
1/5 fps = 1 frame per 5 seconds
1/10 fps = 1 frame per 10 seconds

10 original fps
Realistic     sampling per hour         sampling per min          sampling per second 
       mod 1000      500      250     |  100  50   40      20   |  10    5     2       1     source_fps / sample_fps 
sample fps 1/(10*10) 1/(5*10) 1/(5*5) |  1/10 1/5  1/(2*2) 1/2  |  1     2     5       10
sample fpm 0.6       1.2      2.4     |  6    12   15      30   |  60    120   300     600
sample fph 36        72       144     |  360  720  900     1800 |  3600  7200  18000   36000
1-10 fps, 1-600 fpm, 1-36000 fph

Nice numbers with factors (and multiples of factors) for original fps
warn about bad sampling rates (modulo with weird numbers, provide factors that work well?)

incoming sampling vs original

outgoing sampling == ffmpeg inputs
'''

def determine_sampling_modulo(source_fps, sampling_rate, sampling_time):
  #sampling_time = 0 for seconds, 1 for minutes, 2 for hours

  print('Original video: {0} fps'.format(source_fps))
  #Convert to fps
  if sampling_time > 0:
    sampling_fps = sampling_rate / (60 ** sampling_time)
    print('Sampling at {0} fps based on input of {1} fp{2}'.format(sampling_fps, sampling_rate, 'm' if sampling_time == 1 else 'h'))
  else:
    sampling_fps = sampling_rate
    print('Sampling at {0} fps'.format(sampling_fps))


  modulo = source_fps / sampling_fps 
  #Deal with gross numbers
  if modulo % 1 != 0: 
    print('Modulo {0} wont work, Sampling fps adjusted to {1}'.format(modulo, source_fps / int(modulo)))

  #XXX Floors gross numbers for now
  modulo = int(modulo)
  print('Using modulo {0} to sample frames'.format(modulo))

  return modulo

if __name__ == '__main__':
  vp = VideoProcessor([flip_frame, flip_frame])
  vp.test_run()
