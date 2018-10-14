import unittest
from mock import MagicMock
from Data_Analysis import DataAnalysis

class Test_DataAnalysis(unittest.TestCase):
    getData = lambda x:0
    myInstanceNumber = 42
    def setUp(self):
        self.myInstance = DataAnalysis(instance=self.myInstanceNumber,
                                       callback=self.getData)

    def test_provideInstance(self):
        self.assertEqual(self.myInstance._instance, self.myInstanceNumber)

    def test_defaultInstanceIsOne(self):
        testInstance = DataAnalysis(callback=self.getData)
        self.assertEqual(testInstance._instance,1)

    def test_fourierTransformData(self):
        pass
