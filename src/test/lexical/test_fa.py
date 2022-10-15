import unittest

from src.lexical.deterministic_finite_automation import DFA
from src.lexical.finite_automation import *
from src.lexical.finite_automation import FA

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

dfa_s = [  # TODO
    DFA(

    ),
    DFA(

    )]  # 用来测试最小化


class FATest(unittest.TestCase):

    def test_get_fa_c_minus(self):
        self.assertTrue(True)
        fa = get_fa_c_minus()
        print(fa)

    def test_fa_s(self):
        for fa in fa_s:
            self.assertTrue(fa.k_and_letters())


if __name__ == '__main__':
    unittest.main()
