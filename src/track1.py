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
driver = Driver()

driver.on()

try:
	while True:
		output = vision.process_frame()
		driver.track(output)		

except KeyboardInterrupt:
	print("stop")
	driver.off()
	vision.destroy()
	pass

