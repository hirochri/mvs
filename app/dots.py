import cv2
import time

#Background = 254 254 254
#Orange = 254 147 110
#Yellow = 253 211 109
#Green = 106 227 129
#Blue = 71 179 240
colors = {
  (254, 147, 110): 'Orange',
  (253, 211, 109): 'Yellow',
  (106, 227, 129): 'Green',
  (71, 179, 240): 'Blue'
}
counts = {color: 0 for color in "Orange.Yellow.Green.Blue".split('.')}

def contour_func_count(frame, counts, colors):
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
    if color_tup in colors:
      counts[colors[color_tup]] += 1
  return frame

def contour_func_draw(frame, counts, colors, frame_num):
  print(counts)
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
    if color_tup in colors:
      frame[yy][xx] = (0, 0, 0)
      frame[yy+1][xx] = (0, 0, 0)
      frame[yy-1][xx] = (0, 0, 0)
      frame[yy][xx+1] = (0, 0, 0)
      frame[yy][xx-1] = (0, 0, 0)
      '''
      cv2.imshow('image',frame)
      cv2.waitKey(0)
      '''

  all_str = " ".join(color[0] + ':' + str(count) for color, count in counts.items())

  font = cv2.FONT_HERSHEY_SIMPLEX
  cv2.putText(frame ,'Frame ' + str(frame_num) + ' Dot Count: ' + str(len(contours)),(20, 50), font, 1, (200,255,155), 2, cv2.LINE_AA)
  cv2.putText(frame , all_str, (20, 280), font, 1, (200,255,155), 2, cv2.LINE_AA)
  return frame

if __name__ == '__main__':
  cap = cv2.VideoCapture('dots.mp4')

  frame = cap.read()[1]

  frame = contour_func(frame, counts, colors)
  cv2.imshow('image',frame)
  cv2.waitKey(0)

  cv2.destroyAllWindows()
  cap.release()


