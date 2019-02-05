from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys
import imutils

camera = PiCamera()
camera.resolution = (80, 60)
camera.framerate = 60
rawCapture = PiRGBArray(camera, size=(80, 60))

time.sleep(0.1)
lastTime = time.time() * 1000.0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(image, 100, 200)

    print time.time() * 1000.0 - lastTime
    lastTime = time.time() * 1000.0

    cv2.imshow("Preview", edges)

    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break
