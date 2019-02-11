from __future__ import print_function

import argparse

from vision import Vision
from driver import Driver
import time

print("start")

# parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--display", type=int, default=-1, help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

# vision init
vision = Vision(debug = args["display"])

# init drive
driver = Driver(maxSpeed = 0.8)

driver.on()

P = 0.0045
D = 0.0005
I = 0.0000

try:
	lastError = 0
	integral = 0

	startTime = time.time()
	frames = 0
	fps = 0

	while True:
		
		error = vision.process_frame()
		integral += error
		
		turn = P * error + D * (error - lastError) + I * integral
		lastError = error

		turn = min(1, max(-1, turn))

		driver.track(turn)		

		frames += 1
		now = time.time()
		duration = now - startTime

		if duration >= 1:
			fps = frames / duration
			frames = 0
			startTime = now

		print(str(error) + " -> " + str(turn) + " FPS = " + str(fps))


except KeyboardInterrupt:
	print("stop")
	driver.off()
	vision.destroy()
	pass

