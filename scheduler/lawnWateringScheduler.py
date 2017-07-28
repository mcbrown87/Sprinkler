import datetime
import json
import os
import time

import sys
from dateutil import parser

from weatherWebService import WeatherWebService
from valveWebService import ValveWebService

class LawnWateringScheduler:
	def __init__(self):
		self._duration = lambda : datetime.timedelta(0, 0, 0, 0, ConfigFile(os.path.dirname(os.path.realpath(__file__)) + '/config.json').valveOpenDurationMinutes)
		self._sleepTime = 30
		self._runCriteria = lambda : ConfigFile(os.path.dirname(os.path.realpath(__file__)) + '/config.json').runCriteria
		self._valveWebService = ValveWebService()

	def shouldOpen(self):
		for runCriterion in self._runCriteria():
			if runCriterion.shouldStart():
				return True

		return False

	def shouldClose(self):
		return self._duration() < self._valveWebService.OpenDuration()

	def run(self):
		while(True):
			try:
				if self.shouldOpen():
					self._valveWebService.Open()

				if self.shouldClose():
					self._valveWebService.Close()

				time.sleep(5)
			except:
				e = sys.exc_info()[0]
				with open(os.path.dirname(os.path.realpath(__file__)) + 'scheduler.log', 'a') as file:
					file.write(e)
					file.write("\r\n")

class DependantCriterion:
	def __init__(self, criteria):
		self._criteria = criteria

	def shouldStart(self):
		for criterion in self._criteria:
			if not criterion.shouldStart():
				return False

		return True

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

class EnabledCriterion:
	def __init__(self, shouldStart):
		if shouldStart == 'True':
			self._shouldStart = True

		else:
			self._shouldStart = False

	def shouldStart(self):
		return self._shouldStart

class WeatherCriterion:
	def __init__(self):
		self._weatherWebService = WeatherWebService()

	def shouldStart(self):
		return self._weatherWebService.CurrentWeather() != "Rain"

class ConfigFile:
	def __init__(self, file):
		with open(file) as data_file:
			self._data = json.load(data_file)

	@property
	def runCriteria(self):
		criteria = []

		for day in self._data["days"]:
			for time in self._data["times"]:
				criterion = DependantCriterion([TimeCriterion(parser.parse(time).time()),
				                                DayCriterion(day),
				                                EnabledCriterion(self.enabled),
				                                WeatherCriterion()])
				criteria.append(criterion)

		return criteria

	@property
	def valveOpenDurationMinutes(self):
		return self._data["duration"]

	@property
	def enabled(self):
		return self._data["enabled"]

def main():
	app = LawnWateringScheduler()
	app.run()

if __name__ == "__main__":
	main()