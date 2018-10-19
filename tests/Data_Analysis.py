import scipy.fftpack
import scipy.signal
import matplotlib.pyplot
import numpy as np
import random

class DataAnalysis:
    maxReducedTimeArraySize: int

    def __init__(self,  instance=None, callback=None, cutOffFrequencies=None,
                        integralOrder=None, lengthOfFilter=None):
        self._instance          = instance          if instance != None         else 1
        self.maxReducedTimeArraySize = 50
        # 251 is designed to obtain the sharpest possible cut off, Figure 6.39 from Signals and systems Alan Oppenheimer
        self.lengthOfFilter     = lengthOfFilter    if lengthOfFilter!= None    else 251
        self.cutOffFrequencies  = cutOffFrequencies if cutOffFrequencies!= None else np.array([10])

    def fourierTransform(self, dictMeasurements): # data should be a dictionary including {"data":array, "time":array}
        signal = dictMeasurements["data"]
        time = dictMeasurements["time"]
        fourier = scipy.fftpack.fft(signal)
        samplingFreq = self._tryGetSamplingFreq(time)
        freq = scipy.fftpack.fftfreq(signal.size, samplingFreq)
        return {"signal":signal, "time":time,
                "fourier":fourier, "freq":freq}

    def plot(self, dictMeasurements):
        data = self.fourierTransform(dictMeasurements)
        n = data["freq"].size
        plt = matplotlib.pyplot
        plt.plot(data["freq"][:n//2], abs(data["fourier"][:n//2]))
        plt.grid()
        plt.show()

    def _tryGetSamplingFreq(self, timeArray): # Hz
        med = np.median(self._calcTimeDelta(timeArray))
        return 1/med if not np.isnan(med) else None

    def _calcTimeDelta(self, timeArray):
        return np.diff(self._getReducedTimeArray(timeArray))

    def _getReducedTimeArray(self, timeArray):
        return timeArray[:self.maxReducedTimeArraySize]

    def _createFilter(self):
        return scipy.signal.firwin(self.lengthOfFilter, self.cutOffFrequencies)

if __name__ == '__main__':
    analysis = DataAnalysis()
    data = np.array([])
    time = np.array([])
    for i in range(0,100):
        data = np.append(data, random.uniform(0, 1000))
        time = np.append(time, (i+1))
    analysis.plot({"data":data, "time":time})