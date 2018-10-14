import threading
import time
import numpy as np
import logging
class DataCollection:
    def __init__(self, instance=None, interval_ms=None, span_s=None, callback=None):
        self._instance       = instance if instance != None else 1
        self._interval_ms    = interval_ms if interval_ms != None else 1000
        self._span_s         = span_s if span_s != None else 60
        if not callable(callback): raise Exception("Sample function not provided")
        self._getData        = callback
        self._measurements   = np.array([])
        self._setInterval()
        self._timer          = threading.Timer(self._intervalTime, self._timerInterval)
        self.logger = logging.getLogger("DataCollection."+str(self._instance))
        self.logger.setLevel(logging.INFO)
        mess =  "Instance created of data collection with interval " \
                +str(self._intervalTime) + " sec, and span set as" \
                                           +str(self._span_s) + " sec."
        self.logger.info(msg=mess)

    def _timerInterval(self):
        currTime = time.time()
        self._measurements = np.append(self._measurements, 
                            Measurement(data=self._getData(), 
                                        time=currTime))
        self._tryEraseOldestData(currTime)
        self._timer.start()
    def _tryEraseOldestData(self, currTime):
        oldTime = currTime - self._span_s
        if (self._measurements[0].time <= oldTime):
            self.logger.debug(msg="Erase measurement from time "+str(self._measurements[0].time)\
                              +" at time "+str(currTime))
            self._measurements = np.delete(self._measurements, 0)
    def _setInterval(self):
        self._intervalTime = self._interval_ms/1000.0
    def startSampling(self):
        self._timerInterval()
    def stopSampling(self):
        self._timer.stop()
    def getMeasurements(self):
        return self._measurements
    def getSpan(self):
        return self._span_s
    def changeSpan(self, s=None):
        self._span_s = s if s != None else self._span_s
        self.logger.info(msg="Span changed to "+str(self._span_s)+ " sec")
    def getInterval(self):
        return self._interval_ms
    def changeInterval(self, ms=None):
        self._interval_ms = ms if ms != None else self._interval_ms
        self._setInterval()
        self.logger.info(msg="Interval changed to "+str(self._intervalTime)+ " sec")
        self.stopSampling()
        self.startSampling()


class Measurement:
    def __init__(self, data, time):
        self.data = data
        self.time = time

