import numpy as np
import cv2
import os
import time
from werkzeug.datastructures import FileStorage
import tempfile
from subprocess import Popen, PIPE
from functools import reduce
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import random
from dots import contour_func_draw, contour_func_count

class VideoProcessor:
  def __init__(self, funcs):
    self.funcs = funcs
    self.generated_data = {}
    self.colors = {
      (254, 147, 110): 'Orange',
      (253, 211, 109): 'Yellow',
      (106, 227, 129): 'Green',
      (71, 179, 240): 'Blue'
    }
    self.counts = {color: 0 for color in "Orange.Yellow.Green.Blue".split('.')}

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
        frame = cap.read()[1]

        #Generate data based on all frames
        self.generated_data['frame_count'] = self.generated_data.get('frame_count', 0) + 1
        frame = contour_func_count(frame, self.counts, self.colors)

        if num % sampling_modulo == 0:
          yield (num, frame)
        #Frame number, frame
        #Can calculate timestamp from frame number and fps

      #Release the capture
      cap.release()

    return dimensions, fps, generator

  def process_video(self, input_filename, output_filename, sampling_rate, sampling_time, output_fps=None):
    #TODO decide how to work with filenames/folders.. only pass uuids?

    frame_dimensions, original_fps, frame_generator = self.create_frame_generator(input_filename, sampling_rate, sampling_time)
    output_fps = original_fps if output_fps == None else output_fps

    #0. Potentially tweak output size to accomodate frames being put together
    #Adjust height
    original_dimensions = frame_dimensions
    '''
    frame_dimensions = (frame_dimensions[0], frame_dimensions[1] * 2)
    '''

    #XXX will need to tweak with colors and codecs..
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
        output_filename
    ]

    p = Popen(cmd, stdin=PIPE)

    for num, frame in frame_generator():
      #1. Generate data from sampled frame

      #Apply functions to sampled frame
      #frame = self.apply_functions(frame)
      frame = contour_func_draw(frame, self.counts, self.colors, num)

      #2. Generate data from modified frame

      #Frame composition stuff?
      #3. Potentially create graphs and add them to frames

      #Vertically stack frames -> also needs to change image dimensions
      '''
      print(num)
      graph = random_plot(original_dimensions)
      print(num, 'Graph done')
      frame = np.concatenate((frame, graph), axis=0)
      print(num, 'Concat done')
      '''

      p.stdin.write(frame.tostring())

    print('XXX')
    print(self.generated_data)
    print('XXX')
    #XXX read up on how Popen knows when stdin ends

  def apply_functions(self, frame):
    return reduce(lambda res, func: func(res), self.funcs, frame)

class VideoFunctions:
  def flip(frame):
    return cv2.flip(frame, 0)

def random_plot(dimensions):
  rand_arr = [random.random() for _ in range(50)]
  w, h = dimensions
  my_dpi = 150
  fig = plt.figure(figsize=(w/my_dpi, h/my_dpi), dpi=my_dpi)
  fig.add_subplot()
  ax = fig.subplots()
  ax.plot(rand_arr)
  fig.canvas.draw()
  #plt.show()
  ret = np.array(fig.canvas.renderer._renderer)
  ret_without_alpha = ret[:,:,:3] #hacky RGBA->RGB so that dimensions match frame dimensions (ex: frame.shape == graph.shape)
  plt.close(fig)
  return ret_without_alpha

if __name__ == '__main__':
  funcnames = []
  funcs = [getattr(VideoFunctions, funcname) for funcname in funcnames]
  #vp = VideoProcessor([VideoFunctions.flip])
  vp = VideoProcessor(funcs)
  #vp.process_video('control_2.mp4', 'hirotest.mp4', 10, 0)
  vp.process_video('dots.mp4', 'dotstest.mp4', 5, 0)
