import unittest
import numpy as np
from mock import MagicMock
from Data_Analysis import DataAnalysis
import scipy.fftpack
# from scipy.fftpack import fft, ifft, fftfreq
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
        self.myInstance.tryGetSamplingFreq = MagicMock(return_value=samplingFreq)
        self.myInstance.analyze(self.testData)
        self.myInstance.tryGetSamplingFreq.assert_called_with(self.testData["time"])
        scipy.fftpack.fftfreq.assert_called_with(self.testData["data"].size, samplingFreq)

    def test_returnFourierData(self):
        self.myInstance.tryGetSamplingFreq = MagicMock(return_value=10)
        self.assertEqual(self.myInstance.analyze(self.testData), {"signal":self.testData["data"],
                                                                  "time":self.testData["time"],
                                                                  "fourier":fftReturnVal,
                                                                  "freq":fftFreqReturnVal})

    def test_getSamplingPeriod(self):
        pass

if __name__ == '__main__':
    unittest.main()