import RPi.GPIO as GPIO

class Valve:

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(7, GPIO.OUT)
	GPIO.output(7, GPIO.HIGH)

	def IsOpen(self):
		return not GPIO.input(7)

	def Open(self):
		if(self.IsOpen()):
			return

		GPIO.output(7, GPIO.LOW)

	def Close(self):
		if(not self.IsOpen()):
			return

		GPIO.output(7, GPIO.HIGH)
