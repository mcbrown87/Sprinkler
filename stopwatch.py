import datetime


class Stopwatch:
	def __init__(self):
		self._startTime = datetime.datetime.now()

	def Elapsed(self):
		return datetime.datetime.now() - self._startTime
