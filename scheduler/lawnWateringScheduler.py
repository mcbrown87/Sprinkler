import datetime
import time
from threading import Thread

from scheduler.valveWebService import ValveWebService

class LawnWateringScheduler():
	def __init__(self):
		self._duration = datetime.timedelta(0, 0, 0, 0, 2)
		self._sleepTime = 30
		self._scheduler = Scheduler(datetime.time(7, 1))
		self._valveWebService = ValveWebService()

	def shouldOpen(self):
		return self._scheduler.shouldStart()

	def shouldClose(self):
		return self._duration < self._valveWebService.OpenDuration()

	def run(self):
		while(True):
			if self.shouldOpen():
				self._valveWebService.Open()

			if self.shouldClose():
				self._valveWebService.Close()

			time.sleep(5)


class Scheduler:
	def __init__(self, startTime=None):
		self._startTime =  datetime.time(7) if startTime is None else startTime
		self._currentTimeGetter = lambda : datetime.datetime.now().time().replace(second=0, microsecond=0)

	def shouldStart(self):
		return self._startTime == self._currentTimeGetter()


def main():
	app = LawnWateringScheduler()
	app.run()

if __name__ == "__main__":
		main()