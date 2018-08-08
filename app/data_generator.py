class DataGeneratorTemplate:
  def __init__(self):
    #All data structures used internally
    #Nothing passed around, use self.<x>
    pass

  def capture_data(self, frame):
    #Function run on all frames
    #Needs to return frame
    pass

  def utilize_data(self, frame):
    #Function run on sampled frames
    #Needs to return frame
    pass

import cv2
class DotDataGenerator:
  def __init__(self):
    self.counts = {color: 0 for color in "Orange.Yellow.Green.Blue".split('.')}
    self.colors = {
      (254, 147, 110): 'Orange',
      (253, 211, 109): 'Yellow',
      (106, 227, 129): 'Green',
      (71, 179, 240): 'Blue'
    }
    self.frame_num = -1

  def capture_data(self, frame):
    self.frame_num += 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 100, 255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
    _, contours, _ = cv2.findContours(threshed,1,2)

    #Only take big contours, not tiny ones
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 10]
    for cnt in contours:
      M = cv2.moments(cnt)
      yy = int(M["m01"] / M["m00"])
      xx = int(M["m10"] / M["m00"])
      color_tup = tuple(frame[yy][xx][::-1])
      if color_tup in self.colors:
        self.counts[self.colors[color_tup]] += 1

    return frame

  def utilize_data(self, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 100, 255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
    _, contours, _ = cv2.findContours(threshed,1,2)

    #Only take big contours, not tiny ones
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 10]
    for cnt in contours:
      cv2.drawContours(frame, [cnt], 0, (0, 0, 255), 1)
      M = cv2.moments(cnt)
      yy = int(M["m01"] / M["m00"])
      xx = int(M["m10"] / M["m00"])
      color_tup = tuple(frame[yy][xx][::-1])
      if color_tup in self.colors:
        frame[yy][xx] = (0, 0, 0)
        frame[yy+1][xx] = (0, 0, 0)
        frame[yy-1][xx] = (0, 0, 0)
        frame[yy][xx+1] = (0, 0, 0)
        frame[yy][xx-1] = (0, 0, 0)

    all_str = " ".join(color[0] + ':' + str(count) for color, count in self.counts.items())

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame ,'Frame ' + str(self.frame_num) + ' Dot Count: ' + str(len(contours)),(20, 50), font, 1, (200,255,155), 2, cv2.LINE_AA)
    cv2.putText(frame , all_str, (20, 280), font, 1, (200,255,155), 2, cv2.LINE_AA)
    return frame
