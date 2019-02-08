from gpiozero import Motor, LED
from simple_pid import PID

class Driver:
	def __init__(self):
		self.motorLE = LED(18)
		self.motorRE = LED(13)
		self.motorL = Motor(24, 23)
		self.motorR = Motor(6, 5)

		self.pid = PID(0.01, 0.0, 0.00, setpoint=0)
		self.pid.output_limits = (-1.0, 1.0)

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

	def track(self, error = 0):
		control = self.pid(error)		
		acontrol = abs(control)
		# print(str(error) + " -> " + str(control))

		if control > 0:
			self.motorL.forward(acontrol)
			self.motorR.backward(acontrol)
		else:
			self.motorL.backward(acontrol)
			self.motorR.forward(acontrol)
