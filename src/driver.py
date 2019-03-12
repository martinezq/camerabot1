from gpiozero import Motor, LED
# from simple_pid import PID

class Driver:
	def __init__(self, maxSpeed = 1.0, acc = 0.005):
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

	def track(self, turn = 0, speed = 1):

		targetSpeed = max(0.25, self.maxSpeed - abs(turn)/2)

		if targetSpeed < self.actualSpeed:
			self.actualSpeed -= 2 * self.acc
		else:
			self.actualSpeed += self.acc

		self.actualSpeed = min(self.maxSpeed, self.actualSpeed)

		motorSpeed = min(speed, self.actualSpeed)
		dif = min(abs(turn), self.actualSpeed) * 2

		speedL = motorSpeed
		speedR = motorSpeed

		if turn > 0:
			speedR = motorSpeed - dif
		elif turn < 0:
			speedL = motorSpeed - dif
		
		# print("turn = " + str(turn) + ", l = " + str(speedL) + ", r = " + str(speedR))

		self.motorMove(self.motorL, speedL)
		self.motorMove(self.motorR, speedR)


	def motorMove(self, motor, speed):
		if speed >= 0:
			motor.forward(speed)
		else:
			motor.backward(-speed)