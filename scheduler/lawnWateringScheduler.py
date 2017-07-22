import datetime
import time

from scheduler.valveWebService import ValveWebService

class LawnWateringScheduler():
	def __init__(self):
		self._duration = datetime.timedelta(0, 0, 0, 0, 1)
		self._sleepTime = 30
		self._runCriteria = [TimeCriterion(datetime.time(9, 34)), DayCriterion(6)]
		self._valveWebService = ValveWebService()

	def shouldOpen(self):
		for runCriterion in self._runCriteria:
			if not runCriterion.shouldStart():
				return False

		return True

	def shouldClose(self):
		return self._duration < self._valveWebService.OpenDuration()

	def run(self):
		while(True):
			if self.shouldOpen():
				self._valveWebService.Open()

			if self.shouldClose():
				self._valveWebService.Close()

			time.sleep(5)

class TimeCriterion:
	def __init__(self, startTime):
		self._startTime = startTime
		self._currentTimeGetter = lambda : datetime.datetime.now().time().replace(second=0, microsecond=0)

	def shouldStart(self):
		return self._startTime == self._currentTimeGetter()

class DayCriterion:
	def __init__(self, day):
		if day > 6 or day < 0:
			raise ValueError("Invalid day value")

		self._day = day
		self._currentDayGetter = lambda : datetime.datetime.today().weekday()

	def shouldStart(self):
		return self._day == self._currentDayGetter()

def main():
	app = LawnWateringScheduler()
	app.run()

if __name__ == "__main__":
		main()