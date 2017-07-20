import unittest
import time
import datetime
from mock import MagicMock, Mock
from scheduler.lawnWateringScheduler import LawnWateringScheduler, Scheduler

class LawnWateringSchedulerShould(unittest.TestCase):
	def test_open_the_valve_based_on_scheduler(self):
		sut = LawnWateringScheduler()

		mockScheduler = Mock()
		mockScheduler.shouldStart.return_value = True
		sut._scheduler = mockScheduler

		self.assertTrue(sut.shouldOpen())

	def test_not_open_the_valve_based_on_scheduler(self):
		sut = LawnWateringScheduler()

		mockScheduler = Mock()
		mockScheduler.shouldStart.return_value = False
		sut._scheduler = mockScheduler

		self.assertFalse(sut.shouldOpen())

	def test_should_close_after_duration_expired(self):
		sut = LawnWateringScheduler()

		sut._duration = datetime.timedelta(0, 0, 0, 0, 20)

		mockValveWebService = Mock()
		mockValveWebService.OpenDuration.return_value = datetime.timedelta(0, 1, 0, 0, 20)
		sut._valveWebService = mockValveWebService

		self.assertTrue(sut.shouldClose())

	def test_should_not_close_before_duration_expired(self):
		sut = LawnWateringScheduler()

		sut._duration = datetime.timedelta(0, 0, 0, 0, 20)

		mockValveWebService = Mock()
		mockValveWebService.OpenDuration.return_value = datetime.timedelta(0, 0, 0, 0, 10)
		sut._valveWebService = mockValveWebService

		self.assertFalse(sut.shouldClose())

class SchedulerShould(unittest.TestCase):
	def test_start_at_start_time(self):
		sut = Scheduler()
		sut._startTime = datetime.time(7)
		sut._currentTimeGetter = lambda: datetime.time(7)

		self.assertTrue(sut.shouldStart())

	def test_not_start_after_start_time(self):
		sut = Scheduler()
		sut._startTime = datetime.time(7, 1)
		sut._currentTimeGetter = lambda: datetime.time(7)

		self.assertFalse(sut.shouldStart())

	def test_not_start_before_start_time(self):
		sut = Scheduler()
		sut._startTime = datetime.time(6, 59)
		sut._currentTimeGetter = lambda: datetime.time(7)

		self.assertFalse(sut.shouldStart())

if __name__ == '__main__':
	unittest.main()
