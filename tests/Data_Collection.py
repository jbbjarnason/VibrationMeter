import numpy as np
import logging
import time
class DataCollection:
    def __init__(self, instance=None, period_s=None):
        self._instance       = instance if instance != None else 1
        self._period_s         = period_s if period_s != None else 60
        self._measurements   = Measurements()
        self.logger = logging.getLogger("DataCollection."+str(self._instance))
        self.logger.setLevel(logging.INFO)
        mess =  "Instance created of data collection with time period " \
                                           +str(self._period_s) + " sec."
        self.logger.info(msg=mess)
    def _tryEraseOldestData(self, currTime):
        oldTime = currTime - self._period_s
        if (self._measurements.tryGetFirstTime() <= oldTime):
            self.logger.debug(msg="Erase measurement from time " + str(self._measurements.time[0]) \
                                  + " at time " + str(currTime))
            self._measurements.delete(0)
    def getData(self):
        self.logger.info(msg="Returning "+str(len(self._measurements))+ " items of data")
        return {"data":self._measurements.data, "time":self._measurements.time}
    def push(self, value):
        if not isinstance(value, (int, float, complex)):
            self.logger.error("Push was called with "+str(value)+" type "+str(type(value))+". Number expected.")
            return
        currTime = time.time()
        self._measurements.append(value, currTime)
        self._tryEraseOldestData(currTime)
    def getPeriod(self):
        return self._period_s
    def changePeriod(self, s=None):
        self._period_s = s if s != None else self._period_s
        self.logger.info(msg="Period changed to " + str(self._period_s) + " sec")

class Measurements:
    def __init__(self):
        self.data = np.array([])
        self.time = np.array([])
    def append(self, data1, time):
        print("data")
        print(self.data)
        print("time")
        print(self.time)
        self.data = np.append(self.data, data1)
        self.time = np.append(self.time, time)
    def delete(self, index):
        self.data = np.delete(self.data, index)
        self.time = np.delete(self.time, index)
    def tryGetFirstTime(self):
        return self.time[0] if len(self.time) > 0 else -1
    def __len__(self):
        return len(self.data)


