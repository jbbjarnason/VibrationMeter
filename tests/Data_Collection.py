import threading
import time
import numpy as np
class DataCollection:
    def __init__(self, instance=None, interval_ms=None, callback=None):
        self.instance       = instance if instance != None else 1
        self.interval_ms    = interval_ms if interval_ms != None else 1000
        if not callable(callback): raise Exception("Sample function not provided")
        self.getData        = callback
        self.measurements   = np.array([])
        self.intervalTime   = self.interval_ms/1000.0
        self.timer          = threading.Timer(self.intervalTime, self._timerInterval)
    
    def _timerInterval(self):
        self.measurements = np.append(self.measurements, 
                            Measurement(data=self.getData(), time=time.time()))
        self.timer.start()
    def startSampling(self):
        self._timerInterval()
    def stopSampling(self):
        self.timer.stop()

class Measurement:
    def __init__(self, data, time):
        self.data = data
        self.time = time

