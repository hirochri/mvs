import subprocess
import cv2
import numpy as np
from PIL import Image #PIL needs to be 5.0.0
import time
from subprocess import Popen, PIPE

cap = cv2.VideoCapture('./control_2.mp4')
#width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

cmd = 'ffmpeg -f image2pipe -vcodec png -framerate 10 -i - -vcodec mpeg4 -framerate 10 -preset ultrafast i2p_video.mp4'
p = Popen(cmd.split(), stdin=PIPE)
for _ in range(num_frames):
  frame = cap.read()[1]
  img = Image.fromarray(frame)
  #img.save('./image.png')
  img.save(p.stdin, 'PNG')

#Release the capture
cap.release()
cv2.destroyAllWindows()

