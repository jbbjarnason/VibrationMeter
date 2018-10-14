from scipy.fftpack import fft, ifft

class DataAnalysis:
    def __init__(self, instance=None, callback=None, samplingFreq=None,
                 lowPassFreq=None, highPassFreq=None, integralOrder=None):
        self._instance       = instance if instance != None else 1

    def analyze(self):
        pass