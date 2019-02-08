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
		print("frame")
		frame = self.vs.read()
		wrapped = self.perspective_warp(frame)
		gray = cv2.cvtColor(wrapped, cv2.COLOR_BGR2GRAY)
		ret,thresholded = cv2.threshold(gray, 32, 255, cv2.THRESH_BINARY)
		
		kernel = np.ones((5, 5),np.uint8)
		erosion = cv2.erode(thresholded, kernel, iterations = 1)

		output = 0

		self.mark(erosion, wrapped)

		if self.debug == 1:
			cv2.imshow("Frame", wrapped)
			# cv2.imshow("Frame2", thresholded)
			key = cv2.waitKey(1) & 0xFF

		return output

	def mark(self, img, canvas, x1 = 0, y1 = 0, x2 = None, y2 = None, val = None):
		if x2 is None:
			x2 = self.width

		if y2 is None:
			y2 = self.height * 2
		
		size = x2 - x1

		if val is None:
			val = np.mean(img, axis=(0, 1))
		
		# print(str(val))

		mx = (x2+x1) / 2
		my = (y2+y1) / 2

		mmx1 = (mx + x1) / 2
		mmx2 = (mx + x2) / 2
		mmy1 = (my + y1) / 2
		mmy2 = (my + y2) / 2

		lt = rt = lb = rb = md = 0

		if size > 16:
			lt = img[y1:my, x1:mx].mean(axis=0).mean(axis=0)
			rt = img[y1:my, mx:x2].mean(axis=0).mean(axis=0)
			lb = img[my:y2, x1:mx].mean(axis=0).mean(axis=0)
			rb = img[my:y2, mx:x2].mean(axis=0).mean(axis=0)
			md = img[mmy1:mmy2, mmx1:mmx2].mean(axis=0).mean(axis=0)

		if lt > val:
			self.mark(img, canvas, x1, y1, mx, my, lt)	
		
		if rt > val:
			self.mark(img, canvas, mx, y1, x2, my, rt)

		if lb > val:
			self.mark(img, canvas, x1, my, mx, y2, lb)

		if rb > val:
			self.mark(img, canvas, mx, my, x2, y2, rb)

		if md > val:
			self.mark(img, canvas, mmx1, mmy1, mmx2, mmy2, md)

		if max(lt, rt, lb, rb, md) <= val:
		# if val > 200:
			cv2.rectangle(canvas, (x1, y1), (x2, y2), (0, 255, 0), 2)

		return val

	def perspective_warp(self, img):
		src=np.float32([(0, 0.25), (1, 0.25), (0, 1), (1, 1)]),
		dst=np.float32([(-0.3, 0), (1.3, 0), (0, 1), (1,1)])
		dst_size=(self.width, self.height * 2)
		
		img_size = np.float32([(img.shape[1],img.shape[0])])
		src = src * img_size
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