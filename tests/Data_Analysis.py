from scipy.fftpack import fft, ifft
import numpy as np
import random

class DataAnalysis:
    def __init__(self, instance=None, callback=None, samplingFreq=None,
                 lowPassFreq=None, highPassFreq=None, integralOrder=None):
        self._instance       = instance if instance != None else 1

    def analyze(self, dictMeasurements, samplingFreq): # data should be a dictionary including {"data":array, "time":array}
        data = dictMeasurements["data"]
        numberOfSamples = len(data)
        xAxisTimeDomain = np.linspace(0, numberOfSamples*samplingFreq, numberOfSamples) # for testing
        dataFrequencyDomain = fft(data)
        xAxisFreqDomain = np.linspace(0.0, 1.0/(2.0*samplingFreq), numberOfSamples//2)
        import matplotlib.pyplot as plt
        plt.plot(xAxisFreqDomain, 2.0 / numberOfSamples * np.abs(dataFrequencyDomain[0:numberOfSamples // 2]))
        plt.grid()
        plt.show()

# import numpy as np
# from scipy.fftpack import fft
# # Number of sample points
# N = 600
# # sample spacing
# T = 1.0 / 800.0
# x = np.linspace(0.0, N*T, N)
# y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
# yf = fft(y)
# xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
# import matplotlib.pyplot as plt
# plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
# plt.grid()
#
#
# plt.show()


if __name__ == '__main__':
    analysis = DataAnalysis()
    data = np.array([])
    time = np.array([])
    for i in range(0,100):
        data = np.append(data, random.uniform(0, 1000))
        time = np.append(time, (i+1))
    analysis.analyze({"data":data, "time":time}, 1/800)