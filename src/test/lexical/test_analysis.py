import unittest

from src.lexical.lexical_analysis import analysis


class LATest(unittest.TestCase):

    def testAnalysis(self):
        self.assertTrue(True)
        res = analysis('sy_s/02_var_defn.sy')
        for i in res:
            print(i)
