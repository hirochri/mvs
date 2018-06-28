import subprocess
import cv2
import numpy as np
from PIL import Image #PIL needs to be 5.0.0
import time
from subprocess import Popen, PIPE

cap = cv2.VideoCapture('./control_2.mp4')
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

'''
cmd = 'ffmpeg -f image2pipe -vcodec png -framerate 10 -i - -vcodec mpeg4 -framerate 10 -preset ultrafast i2p_video.mp4'
p = Popen(cmd.split(), stdin=PIPE)
for _ in range(num_frames):
  frame = cap.read()[1]
  img = Image.fromarray(frame)
  img.save(p.stdin, 'PNG')
'''


#y = overwrite input files
cmd = 'ffmpeg -y -f rawvideo -vcodec rawvideo -s {0}x{1} -pix_fmt rgb24 -r 10 -i - -vcodec mpeg4 hirotest.mp4'.format(w,h)
p = Popen(cmd.split(), stdin=PIPE)
for i in range(num_frames):
  frame = cap.read()[1]
  p.stdin.write(frame.tostring())

cap.release()
