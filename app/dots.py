import cv2
import time


def contour_func(frame):
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  th, threshed = cv2.threshold(gray, 100, 255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
  _, contours, _ = cv2.findContours(threshed,1,2)

  #Only take big contours, not tiny ones
  contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 10]
  for cnt in contours:
    cv2.drawContours(frame, [cnt], 0, (0, 0, 255), 1)



  font = cv2.FONT_HERSHEY_SIMPLEX
  cv2.putText(frame ,'Dot Count: ' + str(len(contours)),(20, 50), font, 1, (200,255,155), 2, cv2.LINE_AA)
  return frame

if __name__ == '__main__':
  cap = cv2.VideoCapture('dots.mp4')

  frame = cap.read()[1]

  frame = contour_func(frame)
  cv2.imshow('image',frame)
  cv2.waitKey(0)

  cv2.destroyAllWindows()
  cap.release()

#Background = 254 254 254
#Orange = 254 147 110
#Yellow = 253 211 109
#Green = 106 227 129
#Blue = 71 179 240
