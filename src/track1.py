from __future__ import print_function

import argparse

from vision import Vision
from driver import Driver

print("start")

# parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--display", type=int, default=-1, help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

# vision init
vision = Vision(debug = args["display"])

# init drive
driver = Driver(maxSpeed = 0.4)

driver.on()

P = 0.01
D = 0.001
I = 0.00001

try:
	lastError = 0
	integral = 0
	while True:
		error = vision.process_frame()
		integral += error
		
		turn = P * error + D * (error - lastError) + I * integral
		lastError = error

		print(str(error) + " -> " + str(turn))

		driver.track(turn)		

except KeyboardInterrupt:
	print("stop")
	driver.off()
	vision.destroy()
	pass

