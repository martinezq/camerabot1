from __future__ import print_function
from webcam import WebcamVideoStream 
import argparse
import imutils
import cv2
import numpy as np
import time
from gpiozero import Motor, LED
from simple_pid import PID

print("start")

motorLE = LED(18)
motorRE = LED(13)
motorL = Motor(24, 23)
motorR = Motor(6, 5)

pid = PID(0.01, 0.0, 0.00, setpoint=32)
pid.output_limits = (-1.0, 1.0)

motorLE.on()
motorRE.on()

motorL.stop()
motorR.stop()

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--display", type=int, default=-1, help="Whether or not frames should be displayed")
args = vars(ap.parse_args())
vs = WebcamVideoStream(src=0, width=80, height=60).start()

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

try:
	kernel = np.ones((5, 5),np.uint8)
	while True:
		frame = vs.read()
		wrapped = perspective_warp(frame)
		gray = cv2.cvtColor(wrapped, cv2.COLOR_BGR2GRAY)
		ret,thresholded = cv2.threshold(gray, 115, 255, cv2.THRESH_BINARY)
		
		erosion = cv2.erode(thresholded, kernel, iterations = 1)

		winW = 16
		winH = 16

		control = 0

		for (x, y, window) in sliding_window(erosion, stepSize=winW, windowSize=(winW, winH)):
			average = erosion[y:y+winH, x:x+winW].mean(axis=0).mean(axis=0)
			if average > 64:
				cv2.rectangle(wrapped, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
				control = pid(x)
				
				print(str(x) + " -> " + str(control))

				if control > 0:
					motorL.forward(abs(control))
					motorR.backward(abs(control))
				else:
					motorL.backward(abs(control))
					motorR.forward(abs(control))

				break

		if args["display"] > 0:
			cv2.imshow("Frame", wrapped)
			# cv2.imshow("Work", erosion)
			key = cv2.waitKey(1) & 0xFF
		

except KeyboardInterrupt:
	print("stop")
	motorL.stop()
	motorR.stop()
	motorLE.off()
	motorRE.off()
	cv2.destroyAllWindows()
	vs.stop()
	pass

