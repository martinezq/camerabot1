from __future__ import print_function
from webcam import WebcamVideoStream 
import argparse
import imutils
import cv2
import numpy as np
import time
from gpiozero import Motor, LED

motorLE = LED(18)
motorRE = LED(13)
motorL = Motor(24, 23)
motorR = Motor(6, 5)

motorLE.on()
motorRE.on()

print("start")

motorL.forward()
motorR.forward()

try:
	while True:
		motorL.forward()
		motorR.forward()
		key = cv2.waitKey(1) & 0xFF

except KeyboardInterrupt:
	print("stop")
	motorL.stop()
	motorR.stop()
	motorLE.off()
	motorRE.off()
	pass
