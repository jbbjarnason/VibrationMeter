import scipy.fftpack
# from scipy.fftpack import fft, ifft, fftfreq
import numpy as np
import random

class DataAnalysis:
    maxReducedTimeArraySize: int

    def __init__(self, instance=None, callback=None, samplingFreq=None,
                 lowPassFreq=None, highPassFreq=None, integralOrder=None):
        self._instance       = instance if instance != None else 1
        self.maxReducedTimeArraySize = 50

    def analyze(self, dictMeasurements): # data should be a dictionary including {"data":array, "time":array}
        signal = dictMeasurements["data"]
        time = dictMeasurements["time"]
        fourier = scipy.fftpack.fft(signal)
        samplingFreq = self._tryGetSamplingFreq(time)
        freq = scipy.fftpack.fftfreq(signal.size, samplingFreq)
        return {"signal":signal, "time":time,
                "fourier":fourier, "freq":freq}
        # import matplotlib.pyplot as plt
        # f = freq[:numberOfSamples // 2]
        # s = abs(fourierOfSignal[:numberOfSamples // 2])
        # plt.plot(f, s)
        # plt.grid()
        # plt.show()

    def _tryGetSamplingFreq(self, timeArray): # Hz
        med = np.median(self._calcTimeDelta(timeArray))
        return 1/med if not np.isnan(med) else None

    def _calcTimeDelta(self, timeArray):
        return np.diff(self._getReducedTimeArray(timeArray))

    def _getReducedTimeArray(self, timeArray):
        return timeArray[:self.maxReducedTimeArraySize]

if __name__ == '__main__':
    analysis = DataAnalysis()
    data = np.array([])
    time = np.array([])
    for i in range(0,100):
        data = np.append(data, random.uniform(0, 1000))
        time = np.append(time, (i+1))
    analysis.analyze({"data":data, "time":time}, 1/800)