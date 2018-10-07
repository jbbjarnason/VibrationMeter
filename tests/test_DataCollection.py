import unittest
from Data_Collection import DataCollection

class Test_TestIncrementDecrement(unittest.TestCase):
    def test_provideInstance(self):
        for i in range(1,10):
            testInstance = DataCollection(i)
            self.assertEqual(testInstance.instance,i)

if __name__ == '__main__':
    unittest.main()
