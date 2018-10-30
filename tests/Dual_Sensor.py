from Data_Collection import DataCollection

import RPi
GPIO = RPi.GPIO

class DualSensor:
    def __init__(self, pin1=11, pin2=12):
        GPIO.setmode(GPIO.BOARD)
        self._collector = DataCollection(period_s=120)
        self._createInput(pin1, self.newstate)
        # self._createInput(pin2, self.newstate)

    def _createInput(self, boardPin, cb):
        GPIO.setup(boardPin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.remove_event_detect(boardPin)
        rising = lambda :cb(True)
        falling = lambda :cb(False)
        RPi.GPIO.add_event_detect(boardPin, GPIO.RISING, callback=rising, bouncetime=50)
        RPi.GPIO.add_event_detect(boardPin, GPIO.FALLING, callback=falling, bouncetime=50)
    def newstate(self, state):
        self._collector.push(state)

if __name__ == '__main__':
    pass
    