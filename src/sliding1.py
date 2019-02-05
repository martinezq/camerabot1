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
					 src=np.float32([(0, 0.25), (1, 0.25), (0, 1), (1, 1)]),
					 dst=np.float32([(-0.3, 0), (1.3, 0), (0, 1), (1,1)])):
	img_size = np.float32([(img.shape[1],img.shape[0])])
	src = src* img_size
	dst = dst * np.float32(dst_size)
	M = cv2.getPerspectiveTransform(src, dst)
	warped = cv2.warpPerspective(img, M, dst_size)
	return warped

def sliding_window(image, stepSize, windowSize):
	# slide a window across the image
	for y in range(0, image.shape[0], stepSize):
		for x in range(0, image.shape[1], stepSize):
			# yield the current window
			yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])

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
	#blured = cv2.medianBlur(wrapped, 5)

	cropped = thresholded #[0:115, 0:80]

	kernel = np.ones((5, 5),np.uint8)
	erosion = cv2.erode(cropped, kernel, iterations = 1)
	#dilation = cv2.dilate(cropped,kernel,iterations = 1)
	logTime("erosion")

	winW = 16
	winH = 16

	for (x, y, window) in sliding_window(erosion, stepSize=winW, windowSize=(winW, winH)):
		# if the window does not meet our desired window size, ignore it
		if window.shape[0] != winW or window.shape[1] != winH:
			continue

		average = erosion[y:y+winH, x:x+winW].mean(axis=0).mean(axis=0)
		if average > 64:
			cv2.rectangle(wrapped, (x, y), (x + winW, y + winH), (0, 255, 0), 2)

	if args["display"] > 0:
		cv2.imshow("Frame", wrapped)
		cv2.imshow("Work", erosion)
		logTime("display frame")

		key = cv2.waitKey(1) & 0xFF



cv2.destroyAllWindows()
vs.stop()
