import unittest
import threading
from mock import MagicMock

threading.Timer = MagicMock()
from Data_Collection_Periodic import DataCollectionPeriodic


class Test_DataCollectionPeriodic(unittest.TestCase):
    sample = lambda x: 0
    myInstanceNumber = 42
    myInterval = 1234
    myPeriod = 42
    myInstance = 0

    def setUp(self):
        self.myInstance = DataCollectionPeriodic(instance=self.myInstanceNumber,
                                                 interval_ms=self.myInterval,
                                                 period_s=self.myPeriod,
                                                 callback=self.sample)
        self.myInstance._timer.start = MagicMock()
        self.myInstance._timer.stop = MagicMock()

    def test_provideInterval(self):
        self.assertEqual(self.myInstance._interval_ms, self.myInterval)

    def test_defaultIntervalOneSec(self):
        testInstance = DataCollectionPeriodic(callback=self.sample)
        self.assertEqual(testInstance._interval_ms, 1000)

    def test_provideSampleFunction(self):
        testInstance = DataCollectionPeriodic(callback=self.sample)
        self.assertTrue(callable(testInstance._getData))

    def test_defaultSampleFunctionRaiseError(self):
        with self.assertRaises(Exception): DataCollectionPeriodic()

    def test_raiseErrorIfCallbackIsNotCallable(self):
        with self.assertRaises(Exception): DataCollectionPeriodic(callback=1)

    def test_createTimer(self):
        threading.Timer.assert_called_with(self.myInterval / 1000.0, self.myInstance._timerInterval)

    def test_startDataSampling(self):
        self.myInstance.startSampling()
        self.myInstance._timer.start.assert_called_with()

    def test_stopDataSampling(self):
        self.myInstance.stopSampling()
        self.myInstance._timer.stop.assert_called_with()

    def test_onTimerIntervalStoreFetchedData(self):
        self.myInstance._getData = MagicMock(return_value=42)
        self.myInstance.push = MagicMock()
        self.myInstance._timerInterval()
        self.myInstance.push.assert_called_with(42)

    def test_getInterval(self):
        self.assertEqual(self.myInstance._interval_ms, self.myInstance.getInterval())

    def test_changeInterval(self):
        self.myInstance.changeInterval(465)
        self.assertEqual(self.myInstance._interval_ms, 465)

    def test_changeIntervalRestartsTimer(self):
        self.myInstance._setInterval = MagicMock()
        self.myInstance.stopSampling = MagicMock()
        self.myInstance.startSampling = MagicMock()
        self.myInstance.changeInterval(465)
        self.myInstance._setInterval.assert_called()
        self.myInstance.stopSampling.assert_called()
        self.myInstance.startSampling.assert_called()

    def test_onlyChangeIntervalIfProvided(self):
        last = self.myInstance._interval_ms
        self.myInstance.changeInterval()
        self.assertEqual(self.myInstance._interval_ms, last)

if __name__ == '__main__':
    unittest.main()
