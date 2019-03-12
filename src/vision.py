from webcam import WebcamVideoStream 
import imutils
import cv2
import numpy as np
import time
import math

class Vision:
	def __init__(self, width=80, height=60, debug=0):
		self.width = width
		self.height = height
		self.debug = debug
		self.vs = WebcamVideoStream(src=0, width=width, height=height).start()

	def destroy(self):
		cv2.destroyAllWindows()
		self.vs.stop()

	def process_frame(self):
		# print("frame")

		frame = self.vs.read()

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		ret,thresholded = cv2.threshold(gray, 32, 255, cv2.THRESH_BINARY)

		output = 0

		base = thresholded
		canvas = frame

		output = self.calcualteError(base, canvas)

		if self.debug == 1:
			cv2.imshow("Frame", canvas)
			cv2.imshow("Frame2", base)
			key = cv2.waitKey(1) & 0xFF

		return output

	def calcualteError(self, img, canvas):
		levelRef = 220
		
		width = img.shape[1]
		height = img.shape[0]

		steph = height / 4
		stepw = width / 8

		error = 0

		for y in range(0, height, steph):
			x1 = -1
			x2 = -1
			means = img[y:y+steph].mean(axis=0)
			
			for x in range(0, width, stepw):
				level = means[x:x+stepw].mean(axis=0)
				if level < levelRef and x1 == -1:
					x1 = x
				if level < levelRef and x1 > -1:
					x2 = x + stepw
			
			if x1 > -1:
				if self.debug == 1:
					cv2.rectangle(canvas, (x1, y), (x2, y + steph), (0, 255, 0), 2)

				cx = (x1 + x2) / 2
				de = cx - width/2
				error += de * math.log(y + 4)
				break

		if self.debug == 1:
			cv2.line(canvas, (width/2, height), (width/2 + int(error/10), 0), (0, 0, 255), 2)
		
		return error

def sliding_window(image, stepsteph, windowsteph):
	# slide a window across the image
	for y in range(0, image.shape[0], stepsteph):
		for x in range(0, image.shape[1], stepsteph):
			# yield the current window
			yield (x, y, image[y:y + windowsteph[1], x:x + windowsteph[0]])