from webcam import WebcamVideoStream 
import imutils
import cv2
import numpy as np
import time

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
		ret,thresholded = cv2.threshold(gray, 63, 255, cv2.THRESH_BINARY)

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
		
		width = img.shape[0]
		height = img.shape[1]

		size = width / 4

		error = 0

		for y in range(0, width, size):
			x1 = -1
			x2 = -1
			for x in range(0, height, size / 2):
				level = img[y:y+size, x:x+size].mean(axis=0).mean(axis=0)
				if level < levelRef and x1 == -1:
					x1 = x
				if level < levelRef and x1 > -1:
					x2 = x
			
			if x1 > -1:
				cv2.rectangle(canvas, (x1, y), (x2, y + size), (0, 255, 0), 2)
				cx = (x1 + x2) / 2
				de = cx - width/2
				error += de #* (height - y) / size
				break

		cv2.line(canvas, (width/2, height), (width/2 + error/10, 0), (0, 0, 255), 2)
		return error

def sliding_window(image, stepSize, windowSize):
	# slide a window across the image
	for y in range(0, image.shape[0], stepSize):
		for x in range(0, image.shape[1], stepSize):
			# yield the current window
			yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])