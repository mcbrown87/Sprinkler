import RPi.GPIO as GPIO
import datetime
from stopwatch import Stopwatch


class Valve:

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(7, GPIO.OUT)
	GPIO.output(7, GPIO.HIGH)

	def __init__(self):
		self._stopwatch = None

	def IsOpen(self):
		return not GPIO.input(7)

	def Open(self):
		if(self.IsOpen()):
			return

		GPIO.output(7, GPIO.LOW)
		self._stopwatch = Stopwatch()

	def Close(self):
		if(not self.IsOpen()):
			return

		GPIO.output(7, GPIO.HIGH)
		self._stopwatch = None

	def ValveOpenDuration(self):
		return datetime.timedelta() if self._stopwatch == None else self._stopwatch.Elapsed()