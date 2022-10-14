import unittest
from src.main.lexical.FA import *

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_get_fa_c_minus(self):
        fa=get_fa_c_minus()
        print(fa)

if __name__ == '__main__':
    unittest.main()
