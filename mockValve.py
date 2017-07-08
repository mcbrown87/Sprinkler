import datetime
from stopwatch import Stopwatch

class Valve:
	def __init__(self):
		self._isOpen = False
		self._stopwatch = None

	def IsOpen(self):
		return self._isOpen

	def Open(self):
		if(self.IsOpen()):
			return

		self._isOpen = True
		self._stopwatch = Stopwatch()

	def Close(self):
		if(not self.IsOpen()):
			return

		self._isOpen = False
		self._stopwatch = None

	def ValveOpenDuration(self):
		return datetime.timedelta() if self._stopwatch == None else self._stopwatch.Elapsed()