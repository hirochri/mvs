import numpy as np
import cv2
import os
import time
from werkzeug.datastructures import FileStorage
import tempfile
from subprocess import Popen, PIPE

class VideoProcessor:
  def test_run(self):
    f = open('control_2.mp4', 'rb')
    #Simulates how file comes in via flask/werkzeug
    file = FileStorage(f)

    ###################
    self.process_video(file)
    ###################

    f.close()

  def create_frame_generator(self, filename):
    cap = cv2.VideoCapture(filename)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    #seconds = num_frames / self.fps
    self.fps = int(cap.get(cv2.CAP_PROP_FPS))
    self.w, self.h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def return_func():
      for _ in range(num_frames):
        yield cap.read()[1]

      #Release the capture
      cap.release()

    return return_func

  @profile
  def process_video(self, file):
    with tempfile.TemporaryDirectory() as dirpath:
      filename = os.path.join(dirpath, 'input.mp4')
      file.save(filename)

      frame_generator = self.create_frame_generator(filename)

      cmd = [
          'ffmpeg', '-y', #Overwrite input files
          '-f', 'rawvideo', 
          '-vcodec', 'rawvideo',
          '-s', '{0}x{1}'.format(self.w, self.h),
          '-pix_fmt', 'rgb24',
          '-r', str(self.fps),
          '-i', '-',
          '-an', #Expect no audio
          '-vcodec', 'mpeg4',
          'hirotest.mp4'
      ]
      #scmd = 'ffmpeg -y -f rawvideo -vcodec rawvideo -s {0}x{1} -pix_fmt rgb24 -r {2} -i - -an -vcodec mpeg4 hirotest.mp4'.format(self.w,self.h, self.fps)
      #cmd = scmd.split()
      p = Popen(cmd, stdin=PIPE)

      #1 frame per min -> 30 fps
      #Select on both sides
      #Email from form
      #4 videos -> 1 video with 4 frames
      #Save raws
      #Map multiple functions over raw
      #generate data while processing freames
      #func(frame, timestamp) -> number
      #keep time, number pairs together
      #charts on top, videos on bottom
      #docker different "blocks", so not pip install every time python file changes, see if something similar for NPM
      for frame in frame_generator():
        p.stdin.write(self.apply_changes(frame).tostring())
        #apply_changes to generator or here?

      #XXX read up on how Popen knows when stdin ends

  def apply_changes(self, frame):
    return cv2.flip(frame, 0)

if __name__ == '__main__':
  vp = VideoProcessor()
  vp.test_run()
