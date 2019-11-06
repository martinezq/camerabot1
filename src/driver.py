from gpiozero import Motor, LED
# from simple_pid import PID

class Driver:
	def __init__(self, maxSpeed = 1.0, acc = 0.01):
		self.motorLE = LED(18)
		self.motorRE = LED(13)
		self.motorL = Motor(24, 23)
		self.motorR = Motor(6, 5)

		self.maxSpeed = maxSpeed
		self.acc = acc
		self.actualSpeed = 0.2

		self.off()

	def stop(self):
		self.motorL.stop()
		self.motorR.stop()

	def on(self):
		self.motorLE.on()
		self.motorRE.on()

	def off(self):
		self.motorLE.off()
		self.motorRE.off()

	def track(self, turn = 0):

		speedL = self.maxSpeed + turn
		speedR = self.maxSpeed - turn

		speedL = max(0, min(speedL, self.maxSpeed))
		speedR = max(0, min(speedR, self.maxSpeed))

		self.motorMove(self.motorL, speedL)
		self.motorMove(self.motorR, speedR)


	def motorMove(self, motor, speed):
		if speed >= 0:
			motor.forward(speed)
		else:
			motor.backward(-speed)