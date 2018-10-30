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

    def test_capMeasurementsSize(self):
        self.myInstance._period_s = 50
        often = self.myInstance._period_s * 2
        for i in range(0,often):
            self.myInstance._measurements.append(i, i)
            self.myInstance._tryEraseOldestData(i)
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

    def test_pushDataAppendToData(self):
        self.myInstance.push(1)
        self.assertEqual(len(self.myInstance._measurements), 1)

    def test_pushDataStoresPushedData(self):
        self.myInstance.push(42)
        self.assertEqual(self.myInstance._measurements.data[0], 42)

    def test_pushDataStoreTimeStamp(self):
        time.time = MagicMock(return_value=43)
        self.myInstance.push(456486)
        self.assertEqual(self.myInstance._measurements.time[0], 43)

    def test_pushDataStoreAmountOfData(self):
        often = 9
        for i in range(0, often):
            myData = random.uniform(0, 1456315)
            myTime = i
            self.myInstance._getData = MagicMock(return_value=myData)
            time.time = MagicMock(return_value=myTime)
            self.myInstance.push(myData)
            self.assertEqual(self.myInstance._measurements.data[i], myData)
            self.assertEqual(self.myInstance._measurements.time[i], myTime)
        self.assertEqual(len(self.myInstance._measurements.data), often)

    def test_pushTriesToEraseOldestData(self):
        time.time = MagicMock(return_value=43)
        self.myInstance._tryEraseOldestData = MagicMock()
        self.myInstance.push(1)
        self.myInstance._tryEraseOldestData.assert_called_with(time.time())

    def test_pushOnlyAcceptsNumericValue(self):
        self.myInstance.logger.error= MagicMock()
        self.myInstance._measurements.append =MagicMock()
        self.myInstance.push("string")
        self.myInstance.logger.error.assert_called()
        self.myInstance._measurements.append.assert_not_called()


if __name__ == '__main__':
    unittest.main()
