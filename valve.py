import RPi.GPIO as GPIO

class Valve:

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(7, GPIO.OUT)
	GPIO.output(7, GPIO.HIGH)

	def IsOpen():
		return GPIO.input(7)
