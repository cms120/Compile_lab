import unittest

from src.lexical.lexical_analysis import analysis


class LATest(unittest.TestCase):

    def testAnalysis(self):
        self.assertTrue(True)
        res = analysis('test1.sy')
        print(res)
