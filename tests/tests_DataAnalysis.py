import unittest
import numpy as np
from mock import MagicMock
from Data_Analysis import DataAnalysis
import scipy.fftpack
import matplotlib.pyplot
fftReturnVal = "fft called"
fftFreqReturnVal = "fftfreq called"
scipy.fftpack.fft = MagicMock(return_value=fftReturnVal)
scipy.fftpack.fftfreq = MagicMock(return_value=fftFreqReturnVal)

class Test_DataAnalysis(unittest.TestCase):
    getData = lambda x:0
    myInstanceNumber = 42
    testData = {"data":np.array([1.2,12,465,3,4,698,41,1,84,6,1,85]),
                "time": np.array([1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,1.10,1.11])}
    def setUp(self):
        self.myInstance = DataAnalysis(instance=self.myInstanceNumber,
                                       callback=self.getData)

    def test_provideInstance(self):
        self.assertEqual(self.myInstance._instance, self.myInstanceNumber)

    def test_defaultInstanceIsOne(self):
        testInstance = DataAnalysis(callback=self.getData)
        self.assertEqual(testInstance._instance,1)

    def test_fourierTransformData(self):
        # self.myInstance.tryGetSamplingPeriod = MagicMock(return_value=0.1)
        self.myInstance.analyze(self.testData)
        scipy.fftpack.fft.assert_called_with(self.testData["data"])
    def test_getFreqForFourierTransfor(self):
        samplingFreq = 10 # Hz
        self.myInstance._tryGetSamplingFreq = MagicMock(return_value=samplingFreq)
        self.myInstance.analyze(self.testData)
        self.myInstance._tryGetSamplingFreq.assert_called_with(self.testData["time"])
        scipy.fftpack.fftfreq.assert_called_with(self.testData["data"].size, samplingFreq)

    def test_returnFourierData(self):
        self.myInstance._tryGetSamplingFreq = MagicMock(return_value=10)
        self.assertEqual(self.myInstance.analyze(self.testData), {"signal":self.testData["data"],
                                                                  "time":self.testData["time"],
                                                                  "fourier":fftReturnVal,
                                                                  "freq":fftFreqReturnVal})

    def test_getReducedTimeArray(self):
        self.myInstance.maxReducedTimeArraySize = 5
        out = self.myInstance._getReducedTimeArray(self.testData["time"])
        np.testing.assert_array_equal(out, self.testData["time"][:5])
        self.myInstance.maxReducedTimeArraySize = 50
        out = self.myInstance._getReducedTimeArray(self.testData["time"])
        np.testing.assert_array_equal(out, self.testData["time"])

    def test_getTimeDeltaArrayRequestReducedTimeArray(self):
        self.myInstance._getReducedTimeArray = MagicMock()
        timeArray = np.array([1,23,3,4,5,13,415])
        self.myInstance._calcTimeDelta(timeArray)
        self.myInstance._getReducedTimeArray.assert_called_with(timeArray)

    def test_getTimeDeltaArrayRequestReducedTimeArray(self):
        someTime = np.array([1.0,1.2,1.5,1.7,1.9,2.0])
        deltaTime = np.array([0.2,0.3,0.2,0.2,0.1])
        self.myInstance._getReducedTimeArray = MagicMock(return_value=someTime)
        out = self.myInstance._calcTimeDelta("I have already overridden reduced time array returning someTime")
        np.testing.assert_almost_equal(out, deltaTime)

    def test_getSamplingPeriodReturnsNoneWhenTimeArrayEmpty(self): # THROWS Runtime warning, which is actually useful
        self.assertIsNone(self.myInstance._tryGetSamplingFreq(np.array([])))

    def test_getSamplingPeriodRequestReducedTimeArray(self):
        self.myInstance._calcTimeDelta = MagicMock()
        timeArray = np.array([1, 23, 3, 4, 5, 13, 415])
        self.myInstance._tryGetSamplingFreq(timeArray)
        self.myInstance._calcTimeDelta.assert_called_with(timeArray)

    def test_getSamplingPeriodReturnsMedianOfTimeDelta(self):
        deltaTime = np.array([0.2,0.3,0.2,0.2,0.1])
        self.myInstance._calcTimeDelta = MagicMock(return_value=deltaTime)
        out = self.myInstance._tryGetSamplingFreq("I have already overridden delt time array returning deltaTime")
        self.assertEqual(out, 1/np.median(deltaTime))

    def test_locallyPlotFourierTransformationRequestsAnAnalyze(self):
        self.myInstance.analyze = MagicMock()
        self.myInstance.plot(self.testData)
        self.myInstance.analyze.assert_called_with(self.testData)

    def test_locallyPlotFourierTransformationPlots(self):
        myDictonary = dict(signal=np.array([1, 10]), time=np.array([2, 20]), fourier=np.array([-3, -30]), freq=np.array([-4, -40]))
        self.myInstance.analyze = MagicMock(return_value=myDictonary)
        matplotlib.pyplot.plot = MagicMock()
        matplotlib.pyplot.grid = MagicMock()
        matplotlib.pyplot.show = MagicMock()
        self.myInstance.plot(self.testData)
        n = 2
        matplotlib.pyplot.plot.assert_called_with(myDictonary["freq"][:n//2], abs(myDictonary["fourier"][:n//2]))
        matplotlib.pyplot.grid.assert_called()
        matplotlib.pyplot.show.assert_called()


if __name__ == '__main__':
    unittest.main()