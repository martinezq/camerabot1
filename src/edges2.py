from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

vs = WebcamVideoStream(src=0).start()
fps = FPS().start()

while 1 == 1:
	frame = vs.read()
	frame = imutils.resize(frame, width=160)

	edges = cv2.Canny(frame, 100, 200)

	if args["display"] > 0:
		cv2.imshow("Frame", edges)
		key = cv2.waitKey(1) & 0xFF

cv2.destroyAllWindows()
vs.stop()

