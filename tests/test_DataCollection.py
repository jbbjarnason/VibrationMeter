import unittest
import threading
import time
import random
from mock import MagicMock
threading.Timer = MagicMock()
from Data_Collection import DataCollection

class Test_DataCollection(unittest.TestCase):
    sample = lambda x:0
    myInstanceNumber = 42
    myInterval = 1234 
    mySpan = 42
    myInstance = 0 
    def setUp(self):
        self.myInstance = DataCollection(   instance=self.myInstanceNumber, 
                                            interval_ms=self.myInterval, 
                                            span_s=self.mySpan,
                                            callback=self.sample)
        self.myInstance._timer.start = MagicMock()
        self.myInstance._timer.stop = MagicMock()

    def test_provideInstance(self):
        for i in range(1,10):
            testInstance = DataCollection(callback=self.sample, instance=i)
            self.assertEqual(testInstance._instance,i)
    
    def test_defaultInstanceIsOne(self):
        testInstance = DataCollection(callback=self.sample)
        self.assertEqual(testInstance._instance,1)

    def test_provideInterval(self):
        self.assertEqual(self.myInstance._interval_ms,self.myInterval)

    def test_defaultIntervalOneSec(self):
        testInstance = DataCollection(callback=self.sample)
        self.assertEqual(testInstance._interval_ms,1000)

    def test_providesDataSpan(self):
        self.assertEqual(self.myInstance._span_s,self.mySpan)

    def test_defaultIntervalOneSec(self):
        testInstance = DataCollection(callback=self.sample)
        self.assertEqual(testInstance._span_s,60)

    def test_provideSampleFunction(self):
        testInstance = DataCollection(callback=self.sample)
        self.assertTrue(callable(testInstance._getData))

    def test_defaultSampleFunctionRaiseError(self):
        with self.assertRaises(Exception): DataCollection()

    def test_raiseErrorIfCallbackIsNotCallable(self):
        with self.assertRaises(Exception): DataCollection(callback=1)

    def test_createTimer(self):
        threading.Timer.assert_called_with(self.myInterval/1000.0, self.myInstance._timerInterval)

    def test_startDataSampling(self):
        self.myInstance.startSampling()
        self.myInstance._timer.start.assert_called_with()

    def test_stopDataSampling(self):
        self.myInstance.stopSampling()
        self.myInstance._timer.stop.assert_called_with()

    def test_onTimerInterruptAppendToData(self):
        self.myInstance._timerInterval()
        self.assertEqual(len(self.myInstance._measurements), 1)

    def test_onTimerInterruptStoreFetchedData(self):
        self.myInstance._getData = MagicMock(return_value=42)
        self.myInstance._timerInterval()
        self.assertEqual(self.myInstance._measurements.data[0], 42)

    def test_onTimerInterruptStoreTimeStamp(self):
        time.time = MagicMock(return_value=43)
        self.myInstance._timerInterval()
        self.assertEqual(self.myInstance._measurements.time[0], 43)

    def test_onTimerInterruptStoreAmountOfData(self):
        often = 9
        for i in range(0,often):
            myData = random.uniform(0, 1456315)
            myTime = i
            self.myInstance._getData = MagicMock(return_value=myData)
            time.time = MagicMock(return_value=myTime)
            self.myInstance._timerInterval()
            self.assertEqual(self.myInstance._measurements.data[i], myData)
            self.assertEqual(self.myInstance._measurements.time[i], myTime)
        self.assertEqual(len(self.myInstance._measurements.data), often)

    def test_capMeasurementsSize(self): 
        self.myInstance._span_s = 50
        often = self.myInstance._span_s * 2
        for i in range(0,often):
            self.myInstance._getData = MagicMock(return_value=i)
            time.time = MagicMock(return_value=i)
            self.myInstance._timerInterval()
        self.assertEqual(len(self.myInstance._measurements), self.myInstance._span_s)
        self.assertEqual(self.myInstance._measurements.data[0], 50)

    def test_getCurrentData(self):
        pointer, read_only_flag = self.myInstance._measurements.data.__array_interface__['data']
        returnPointer, read_only_flag = self.myInstance.getData().__array_interface__['data']
        self.assertEqual(returnPointer, pointer)

    def test_getSpan(self):
        self.assertEqual(self.myInstance._span_s, self.myInstance.getSpan())
    def test_changeSpan(self):
        self.myInstance.changeSpan(5461)
        self.assertEqual(self.myInstance._span_s, 5461)
    def test_onlyChangeSpanIfProvided(self):
        lastSpan = self.myInstance._span_s
        self.myInstance.changeSpan()
        self.assertEqual(self.myInstance._span_s, lastSpan)

    def test_getInterval(self):
        self.assertEqual(self.myInstance._interval_ms, self.myInstance.getInterval())
    def test_changeInterval(self):
        self.myInstance.changeInterval(465)
        self.assertEqual(self.myInstance._interval_ms, 465)
    def test_changeIntervalRestartsTimer(self):
        self.myInstance._setInterval    = MagicMock()
        self.myInstance.stopSampling    = MagicMock()
        self.myInstance.startSampling   = MagicMock()
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
