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
		frame = self.vs.read()
		wrapped = perspective_warp(frame)
		gray = cv2.cvtColor(wrapped, cv2.COLOR_BGR2GRAY)
		ret,thresholded = cv2.threshold(gray, 115, 255, cv2.THRESH_BINARY)
		
		kernel = np.ones((5, 5),np.uint8)
		erosion = cv2.erode(thresholded, kernel, iterations = 1)

		winW = 16
		winH = 16

		output = 0

		for (x, y, window) in sliding_window(erosion, stepSize=winW, windowSize=(winW, winH)):
			average = erosion[y:y+winH, x:x+winW].mean(axis=0).mean(axis=0)
			if average > 64:
				cv2.rectangle(wrapped, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
				output = x - self.width
				break

		if self.debug == 1:
			cv2.imshow("Frame", wrapped)
			key = cv2.waitKey(1) & 0xFF

		return output
				

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