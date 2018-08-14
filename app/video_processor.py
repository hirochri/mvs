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
from data_generator import DotDataGenerator

class VideoProcessor:
  def __init__(self, funcs, data_generator=None):
    self.funcs = funcs
    self.dg = data_generator

  def get_sampling_modulo(self, source_fps, sampling_rate, sampling_time):
    #sampling_time = 0 for seconds, 1 for minutes, 2 for hours.. -> convert to fps
    sampling_fps = sampling_rate / (60 ** sampling_time)

    print('Original video: {0} fps'.format(source_fps))
    print('Sampling at {0} fps'.format(sampling_fps))

    modulo = source_fps / sampling_fps 

    #Deal with gross numbers temporarily by always flooring the modulo
    if modulo % 1 != 0: 
      print('Modulo {0} wont work, Sampling fps adjusted to {1}'.format(modulo, source_fps / int(modulo)))
    modulo = int(modulo)
    print('Using modulo {0} to sample frames'.format(modulo))

    return modulo

  def create_frame_generator(self, filename, sampling_rate, sampling_time):
    cap = cv2.VideoCapture(filename)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dimensions = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    sampling_modulo = self.get_sampling_modulo(fps, sampling_rate, sampling_time)

    def generator():
      for num in range(num_frames):
        success, frame = cap.read()

        #Generate data based on all frames
        if self.dg:
          frame = self.dg.capture_data(frame)

        if success and num % sampling_modulo == 0:
          yield (num, frame) #Can calculate timestamp from frame number and fps

      #Release the capture
      cap.release()

    return dimensions, fps, generator

  def apply_functions(self, frame):
    return reduce(lambda res, func: func(res), self.funcs, frame)

  #MAIN function that does most of the work
  def process_video(self, input_filename, output_filename, sampling_rate, sampling_time, output_fps=None, composition=False):
    frame_dimensions, original_fps, frame_generator = self.create_frame_generator(input_filename, sampling_rate, sampling_time)
    output_fps = original_fps if output_fps == None else output_fps

    #0. Potentially tweak output size to accomodate frames being put together
    if composition:
      #Save original dimensions and then double height to accomodate for graph
      original_dimensions = frame_dimensions
      frame_dimensions = (frame_dimensions[0], frame_dimensions[1] * 2)

    #XXX ffmpeg can be tough with codecs, colors, etc when
    #used across machines, this will need some tweaking or
    #stricter input/output requirements 
    #The general idea is piping raw video frames straight to 
    #ffmpeg which allows us to get away with not saving images
    #and lets us build videos quickly
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
      #Apply all functions to sampled frame
      frame = self.apply_functions(frame)

      #Work with generated data and write something to frame
      if self.dg:
        frame = self.dg.utilize_data(frame)

      #Frame composition stuff?
      #3. Potentially create graphs and add them to frames
      if composition:
        #For any numpy concatenation, both the frame and the graph
        #need to have identical shape, which is why we altered
        #the frame dimensions earlier 
        #Use <your_nd_array>.shape() to check the dimensions

        #Create random graph and vertically stack it
        #Composition
        graph = random_plot(original_dimensions)
        frame = np.concatenate((frame, graph), axis=0)

      p.stdin.write(frame.tostring())



#Example of how a variety of functions are wrapped in a
#class. These are presented to the users via the 
#video_get_functions function in app.py
class VideoFunctions:
  def flip(frame):
    return cv2.flip(frame, 0)
  
  def invert(frame):
    return cv2.bitwise_not(frame)

#Create a random plot to show data plotting functionality
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

### Demo functions ###

#Show functionality of applying functions to frames
def standard_run():
  funcnames = ['flip', 'invert']
  funcs = [getattr(VideoFunctions, funcname) for funcname in funcnames]
  vp = VideoProcessor(funcs)
  vp.process_video('test_data/cells.test.mp4', 'test_data/cells.out.mp4', 10, 0)

#Show functionality of combining a video and a graph
def graph_run():
  funcnames = []
  funcs = [getattr(VideoFunctions, funcname) for funcname in funcnames]
  vp = VideoProcessor(funcs)
  vp.process_video('test_data/cells.test.mp4', 'test_data/cells.out.mp4', 10, 0, None, True)

#Show functionality of gathering data from all frames
def data_run():
  funcnames = []
  funcs = [getattr(VideoFunctions, funcname) for funcname in funcnames]
  vp = VideoProcessor(funcs, DotDataGenerator())
  vp.process_video('test_data/dots.test.mp4', 'test_data/dots.out.mp4', 10, 0)

if __name__ == '__main__':
  #standard_run()
  #graph_run()
  #data_run()
  print('Please uncomment a demo function')
