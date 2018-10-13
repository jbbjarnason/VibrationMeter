import threading
import time
import numpy as np
class DataCollection:
    def __init__(self, instance=None, interval_ms=None, span_s=None, callback=None):
        self.instance       = instance if instance != None else 1
        self.interval_ms    = interval_ms if interval_ms != None else 1000
        self.span_s         = span_s if span_s != None else 60
        if not callable(callback): raise Exception("Sample function not provided")
        self.getData        = callback
        self.measurements   = np.array([])
        self.intervalTime   = self.interval_ms/1000.0
        self.timer          = threading.Timer(self.intervalTime, self._timerInterval)
    
    def _timerInterval(self):
        currTime = time.time()
        self.measurements = np.append(self.measurements, 
                            Measurement(data=self.getData(), 
                                        time=currTime))
        self._tryEraseOldestData(currTime)
        self.timer.start()
    def _tryEraseOldestData(self, currTime):
        oldTime = currTime - self.span_s
        if (self.measurements[0].time <= oldTime):
            self.measurements = np.delete(self.measurements, 0)
    def startSampling(self):
        self._timerInterval()
    def stopSampling(self):
        self.timer.stop()
    def getMeasurements(self):
        return self.measurements


class Measurement:
    def __init__(self, data, time):
        self.data = data
        self.time = time

