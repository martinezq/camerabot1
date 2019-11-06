from __future__ import print_function

import argparse

from vision import Vision
from driver import Driver
import time
import sys
import signal

def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

print("start")

# parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--display", type=int, default=-1, help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

# vision init
vision = Vision(debug = args["display"])

# init drive
driver = Driver(maxSpeed = 0.6)

driver.on()

P = 0.0300
D = 0.0040
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


finally:
	print("stop")
	driver.off()
	vision.destroy()
	pass
