from __future__ import print_function
from webcam import WebcamVideoStream 
import argparse
import imutils
import cv2
import numpy as np
import time

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--display", type=int, default=-1, help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

vs = WebcamVideoStream(src=0, width=80, height=60).start()

time.sleep(0.1)
lastTime = time.time() * 1000.0

def logTime(msg):
	global lastTime
	print(msg + ": " + str(time.time() * 1000.0 - lastTime))
	lastTime = time.time() * 1000.0

def perspective_warp(img,
					 dst_size=(80, 120),
					 src=np.float32([(0.15, 0.25), (0.85, 0.25), (0, 1), (1, 1)]),
					 dst=np.float32([(0, 0), (1, 0), (0, 1), (1,1)])):
	img_size = np.float32([(img.shape[1],img.shape[0])])
	src = src* img_size
	dst = dst * np.float32(dst_size)
	M = cv2.getPerspectiveTransform(src, dst)
	warped = cv2.warpPerspective(img, M, dst_size)
	return warped

while 1 == 1:
	frame = vs.read()
	logTime("read frame")

	wrapped = perspective_warp(frame)
	logTime("perspective")

	# frame = imutils.resize(frame, width=160)
	# logTime("resize frame")

	gray = cv2.cvtColor(wrapped, cv2.COLOR_BGR2GRAY)
	logTime("grayscale")

	ret,thresholded = cv2.threshold(gray, 115, 255, cv2.THRESH_BINARY)

	# blured = cv2.blur(wrapped, (10, 5))
	blured = cv2.medianBlur(wrapped, 5)

	cropped = blured[0:115, 0:80]

	edges = cv2.Canny(cropped, 50, 150, apertureSize = 3)
	logTime("edges")
	
	minLineLength = 2
	maxLineGap = 0

	lines = cv2.HoughLinesP(edges, 1, np.pi/180, 10, minLineLength, maxLineGap)

	if lines != None:
		for x1,y1,x2,y2 in lines[0]:
				cv2.line(wrapped, (x1, y1), (x2, y2), (0, 255, 0), 2)
	logTime("lines")

	if args["display"] > 0:
		cv2.imshow("Frame", wrapped)
		cv2.imshow("Work", edges)
		logTime("display frame")

		key = cv2.waitKey(1) & 0xFF



cv2.destroyAllWindows()
vs.stop()
