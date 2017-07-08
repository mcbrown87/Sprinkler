import unittest
import time
import datetime

from stopwatch import Stopwatch

class StopwatchShould(unittest.TestCase):
    def test_increase_elapsed_time_after_created(self):
        sut = Stopwatch()
        initialElapsedTime = sut.Elapsed()
        time.sleep(.1)
        self.assertGreater(sut.Elapsed(), initialElapsedTime)

if __name__ == '__main__':
    unittest.main()
