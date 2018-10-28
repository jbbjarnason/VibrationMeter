import unittest
import time
import random
from mock import MagicMock
from Data_Collection import DataCollection

class Test_DataCollection(unittest.TestCase):
    sample = lambda x:0
    myInstanceNumber = 42
    myInterval = 1234 
    myPeriod = 42
    myInstance = 0 
    def setUp(self):
        self.myInstance = DataCollection(   instance=self.myInstanceNumber,
                                            period_s=self.myPeriod)

    def test_provideInstance(self):
        for i in range(1,10):
            testInstance = DataCollection(instance=i)
            self.assertEqual(testInstance._instance,i)
    
    def test_defaultInstanceIsOne(self):
        testInstance = DataCollection()
        self.assertEqual(testInstance._instance,1)

    def test_providesDataPeriod(self):
        self.assertEqual(self.myInstance._period_s,self.myPeriod)

    def test_defaultPeriodOneMin(self):
        testInstance = DataCollection()
        self.assertEqual(testInstance._period_s,60)

    @unittest.skip("Need to implement method in parent before this test")
    def test_capMeasurementsSize(self): 
        self.myInstance._period_s = 50
        often = self.myInstance._period_s * 2
        for i in range(0,often):
            self.myInstance._getData = MagicMock(return_value=i)
            time.time = MagicMock(return_value=i)
            self.myInstance._timerInterval()
        self.assertEqual(len(self.myInstance._measurements), self.myInstance._period_s)
        self.assertEqual(self.myInstance._measurements.data[0], 50)

    def test_getCurrentData(self):
        pointer, read_only_flag = self.myInstance._measurements.data.__array_interface__['data']
        returnPointer, read_only_flag = self.myInstance.getData()["data"].__array_interface__['data']
        self.assertEqual(returnPointer, pointer)

    def test_getPeriod(self):
        self.assertEqual(self.myInstance._period_s, self.myInstance.getPeriod())
    def test_changePeriod(self):
        self.myInstance.changePeriod(5461)
        self.assertEqual(self.myInstance._period_s, 5461)
    def test_onlyChangePeriodIfProvided(self):
        lastPeriod = self.myInstance._period_s
        self.myInstance.changePeriod()
        self.assertEqual(self.myInstance._period_s, lastPeriod)


if __name__ == '__main__':
    unittest.main()
