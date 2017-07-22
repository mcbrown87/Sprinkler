import unittest
import datetime
from mock import MagicMock, Mock
from scheduler.lawnWateringScheduler import LawnWateringScheduler, TimeCriterion, DayCriterion


class LawnWateringSchedulerShould(unittest.TestCase):
	def test_open_the_valve_based_on_criteria(self):
		sut = LawnWateringScheduler()

		mockCriteria = Mock()
		mockCriteria.shouldStart.return_value = True
		sut._runCriteria = [mockCriteria, mockCriteria]

		self.assertTrue(sut.shouldOpen())

	def test_not_open_the_valve_based_on_criteria(self):
		sut = LawnWateringScheduler()

		mockCriteriaShouldStart = Mock()
		mockCriteriaShouldStart.shouldStart.return_value = True

		mockCriteriaShouldNotStart = Mock()
		mockCriteriaShouldNotStart.shouldStart.return_value = False

		sut._runCriteria = [mockCriteriaShouldStart, mockCriteriaShouldNotStart]

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

class TimeCriterionShould(unittest.TestCase):
	def test_start_at_start_time(self):
		sut = TimeCriterion(datetime.time(7))
		sut._currentTimeGetter = lambda: datetime.time(7)

		self.assertTrue(sut.shouldStart())

	def test_not_start_after_start_time(self):
		sut = TimeCriterion(datetime.time(7, 1))
		sut._currentTimeGetter = lambda: datetime.time(7)

		self.assertFalse(sut.shouldStart())

	def test_not_start_before_start_time(self):
		sut = TimeCriterion(datetime.time(6, 59))
		sut._currentTimeGetter = lambda: datetime.time(7)

		self.assertFalse(sut.shouldStart())

class DayCriterionShould(unittest.TestCase):
	def test_fail_with_out_of_range_values_lower_bound(self):
		with self.assertRaises(ValueError):
			DayCriterion(-1)

	def test_fail_with_out_of_range_values_upper_bound(self):
		with self.assertRaises(ValueError):
			DayCriterion(7)

	def test_not_start_on_off_days(self):
		sut = DayCriterion(0)
		sut._currentDayGetter = lambda : 1

		self.assertFalse(sut.shouldStart())

	def test_start_on_on_days(self):
		sut = DayCriterion(0)
		sut._currentDayGetter = lambda : 0

		self.assertTrue(sut.shouldStart())

if __name__ == '__main__':
	unittest.main()
