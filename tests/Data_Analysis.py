from scipy.fftpack import fft, ifft, fftfreq
import numpy as np
import random

class DataAnalysis:
    def __init__(self, instance=None, callback=None, samplingFreq=None,
                 lowPassFreq=None, highPassFreq=None, integralOrder=None):
        self._instance       = instance if instance != None else 1

    def analyze(self, dictMeasurements, samplingPeriod): # data should be a dictionary including {"data":array, "time":array}
        signal = dictMeasurements["data"]
        numberOfSamples = len(signal)
        fourierOfSignal = fft(signal)
        freq = fftfreq(numberOfSamples, samplingPeriod)
        import matplotlib.pyplot as plt
        f = freq[:numberOfSamples // 2]
        s = abs(fourierOfSignal[:numberOfSamples // 2])
        plt.plot(f, s)
        plt.grid()
        plt.show()

if __name__ == '__main__':
    analysis = DataAnalysis()
    data = np.array([])
    time = np.array([])
    for i in range(0,100):
        data = np.append(data, random.uniform(0, 1000))
        time = np.append(time, (i+1))
    analysis.analyze({"data":data, "time":time}, 1/800)