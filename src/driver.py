from gpiozero import Motor, LED
from simple_pid import PID

class Driver:
	def __init__(self):
		self.motorLE = LED(18)
		self.motorRE = LED(13)
		self.motorL = Motor(24, 23)
		self.motorR = Motor(6, 5)

		self.pid = PID(0.01, 0.0, 0.0, setpoint=0)
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
		print(str(error) + " -> " + str(control))

		speed = 0.2

		if control == 0:
			self.motorL.forward(speed)
			self.motorR.forward(speed)
		elif control > 0:
			self.motorL.forward(speed)
			self.motorR.backward(acontrol * 0.2)
		else:
			self.motorL.backward(acontrol * 0.2)
			self.motorR.forward(speed)
