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
        self.myInstance.timer.start = MagicMock()
        self.myInstance.timer.stop = MagicMock()

    def test_provideInstance(self):
        for i in range(1,10):
            testInstance = DataCollection(callback=self.sample, instance=i)
            self.assertEqual(testInstance.instance,i)
    
    def test_defaultInstanceIsOne(self):
        testInstance = DataCollection(callback=self.sample)
        self.assertEqual(testInstance.instance,1)

    def test_provideInterval(self):
        self.assertEqual(self.myInstance.interval_ms,self.myInterval)

    def test_defaultIntervalOneSec(self):
        testInstance = DataCollection(callback=self.sample)
        self.assertEqual(testInstance.interval_ms,1000)

    def test_providesDataSpan(self):
        self.assertEqual(self.myInstance.span_s,self.mySpan)

    def test_defaultIntervalOneSec(self):
        testInstance = DataCollection(callback=self.sample)
        self.assertEqual(testInstance.span_s,60)

    def test_provideSampleFunction(self):
        testInstance = DataCollection(callback=self.sample)
        self.assertTrue(callable(testInstance.getData))

    def test_defaultSampleFunctionRaiseError(self):
        with self.assertRaises(Exception): DataCollection()

    def test_raiseErrorIfCallbackIsNotCallable(self):
        with self.assertRaises(Exception): DataCollection(callback=1)

    def test_createTimer(self):
        threading.Timer.assert_called_with(self.myInterval/1000.0, self.myInstance._timerInterval)

    def test_startDataSampling(self):
        self.myInstance.startSampling()
        self.myInstance.timer.start.assert_called_with()

    def test_stopDataSampling(self):
        self.myInstance.stopSampling()
        self.myInstance.timer.stop.assert_called_with()

    def test_onTimerInterruptAppendToData(self):
        self.myInstance._timerInterval()
        self.assertEquals(len(self.myInstance.measurements), 1)

    def test_onTimerInterruptStoreFetchedData(self):
        self.myInstance.getData = MagicMock(return_value=42)
        self.myInstance._timerInterval()
        self.assertEquals(self.myInstance.measurements[0].data, 42)

    def test_onTimerInterruptStoreTimeStamp(self):
        time.time = MagicMock(return_value=43)
        self.myInstance._timerInterval()
        self.assertEquals(self.myInstance.measurements[0].time, 43)

    def test_onTimerInterruptStoreAmountOfData(self):
        often = 9
        for i in range(0,often):
            myData = getRandomFloat()
            myTime = getRandomFloat()
            self.myInstance.getData = MagicMock(return_value=myData)
            time.time = MagicMock(return_value=myTime)
            self.myInstance._timerInterval()
            self.assertEquals(self.myInstance.measurements[i].data, myData)
            self.assertEquals(self.myInstance.measurements[i].time, myTime)
        self.assertEquals(len(self.myInstance.measurements), often)

    def test_capMeasurementsSize(self): 
        self.myInstance.span_s = 50
        often = self.myInstance.span_s * 2
        for i in range(0,often):
            self.myInstance.getData = MagicMock(return_value=i)
            time.time = MagicMock(return_value=i)
            self.myInstance._timerInterval()
        self.assertEquals(len(self.myInstance.measurements), self.myInstance.span_s)
        self.assertEquals(self.myInstance.measurements[0].data, 50)

def getRandomFloat():
    return random.uniform(0, 1456315)

if __name__ == '__main__':
    unittest.main()
