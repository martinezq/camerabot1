from gpiozero import Motor, LED
# from simple_pid import PID

class Driver:
	def __init__(self, maxSpeed = 1.0):
		self.motorRE = LED(18)
		self.motorLE = LED(13)
		self.motorR = Motor(24, 23)
		self.motorL = Motor(6, 5)

		self.maxSpeed = maxSpeed

		# self.pid = PID(0.01, 0.0, 0.0, setpoint=0)
		# self.pid.output_limits = (-1.0, 1.0)

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
		# control = self.pid(error)		
		# acontrol = abs(control)
		# print(str(error) + " -> " + str(control))

		motorSpeed = min(speed, self.maxSpeed)
		dif = min(abs(turn), self.maxSpeed) * 2

		speedL = motorSpeed
		speedR = motorSpeed

		if turn > 0:
			speedR = motorSpeed - dif
			# speedL = -speedR
		elif turn < 0:
			speedL = motorSpeed - dif
			# speedR = -speedL
		
		print("turn = " + str(turn) + ", l = " + str(speedL) + ", r = " + str(speedR))

		self.motorMove(self.motorL, speedL)
		self.motorMove(self.motorR, speedR)


	def motorMove(self, motor, speed):
		if speed >= 0:
			motor.forward(speed)
		else:
			motor.backward(-speed)