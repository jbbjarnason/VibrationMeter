import sys
import fake_rpi
sys.modules['RPi'] = fake_rpi.RPi # Replace library by fake one
import RPi
GPIO = RPi.GPIO
import unittest
from Dual_Sensor import DualSensor
from mock import MagicMock
RPi.GPIO.setmode = MagicMock()

class Test_DualSensor(unittest.TestCase):
    def setUp(self):
       self.DS = DualSensor()

    def test_createInstance(self):
        self.assertIsNotNone(self.DS)
    def test_initializeGPIO(self):
        RPi.GPIO.setmode.assert_called_with(GPIO.BOARD)
    def test_inputIsDefined(self):
        RPi.GPIO.setup = MagicMock()
        RPi.GPIO.remove_event_detect = MagicMock()
        RPi.GPIO.add_event_detect = MagicMock()
        input = 1
        cb = lambda state:0
        self.DS._createInput(input, cb)
        RPi.GPIO.setup.assert_called_with(input,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        RPi.GPIO.remove_event_detect.assert_called_with(input)
        RPi.GPIO.add_event_detect.assert_called()
        # RPi.GPIO.add_event_detect.assert_called_with(input, GPIO.FALLING, callback=cb, bouncetime=50)
    def test_createDataCollection(self):
        self.assertIsNotNone(self.DS._collector)
    def test_callbackCallsPush(self):
        self.DS._collector.push = MagicMock()
        self.DS.newstate(True)
        self.DS._collector.push.assert_called_with(True)

    def test_createAll(self):
        self.DS._createInput = MagicMock()
        self.DS.__init__()
        self.DS._createInput.assert_called_with(11, self.DS.newstate)
        # self.DS._createInput.assert_called_with(12, self.DS.newstate)
