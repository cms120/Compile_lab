import unittest

from src.lexical.deterministic_finite_automation import *

fa_s = [  # TODO
    FA(  # on ppt 3_2 page22
        k=['S', 'Q', 'U', 'V', 'Z', 'phi'],
        letters=['0', '1'],
        f=[(('S', '0'), ['V', 'Q']),
           (('S', '1'), ['U', 'Q']),
           (('U', '0'), ['phi']),
           (('U', '1'), ['Z']),
           (('V', '0'), ['Z']),
           (('V', '1'), ['phi']),
           (('Q', '0'), ['V', 'Q']),
           (('Q', '1'), ['U', 'Q']),
           (('Z', '0'), ['Z']),
           (('Z', '1'), ['Z'])],

        s='S',
        z=['Z']
    ),
    FA(

    )
]  # 用来测试确定化


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_fa_2_dfa(self):
        self.assertTrue(True)
        for fa in fa_s:
            print(fa_2_dfa(fa))


if __name__ == '__main__':
    unittest.main()
