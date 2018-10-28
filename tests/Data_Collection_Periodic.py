from Data_Collection import DataCollection
import threading
import time
import logging
class DataCollectionPeriodic(DataCollection):
    def __init__(self, instance=None, interval_ms=None, period_s=None, callback=None):
        DataCollection.__init__(self, instance, period_s)
        if not callable(callback): raise Exception("Sample function not provided")
        self._getData        = callback
        self._interval_ms    = interval_ms if interval_ms != None else 1000
        self._setInterval()
        self._timer = threading.Timer(self._intervalTime, self._timerInterval)
        self.logger = logging.getLogger("DataCollectionPeriodic." + str(self._instance))
        self.logger.setLevel(logging.INFO)
        mess = "Periodic data collection fetching data with interval " \
               + str(self._intervalTime) + " sec"
        self.logger.info(msg=mess)
    def _timerInterval(self):
        currTime = time.time()
        self._measurements.append(self._getData(), currTime)
        self._tryEraseOldestData(currTime)
        self._timer.start()
    def _setInterval(self):
        self._intervalTime = self._interval_ms/1000.0
    def startSampling(self):
        self._timerInterval()
    def stopSampling(self):
        self._timer.stop()
    def getInterval(self):
        return self._interval_ms
    def changeInterval(self, ms=None):
        self._interval_ms = ms if ms != None else self._interval_ms
        self._setInterval()
        self.logger.info(msg="Interval changed to "+str(self._intervalTime)+ " sec")
        self.stopSampling()
        self.startSampling()