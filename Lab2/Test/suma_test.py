import unittest
import sys
sys.path.append('C:\\googleMapsVS\\Google-Maps\\Lab2\\Scripts')
from suma import suma

class TestSuma(unittest.TestCase):
    def test_suma(self):
        self.assertEqual(suma(1,2),3) # Asumo que tiene que ser 3
if __name__ == '__main__':
    unittest.main()