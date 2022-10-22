import string

from src.syntax.syntax_unit import SyntaxUnit
from src.util import read_file


class Production:
    def __init__(self, left: SyntaxUnit, right: tuple[SyntaxUnit]):  # 产生式
        self.left = left
        self.right = right

    def __str__(self):
        str_m = self.left.value + ' ->'
        for unit in self.right:
            str_m += ' ' + unit.value
        return str_m

    @staticmethod
    def init_by_string(line: str):
        left_right = line.split(' -> ')
        assert len(left_right) == 2, 'error left_right: ' + line

        right_groups = left_right[1].split(' ')
        assert len(right_groups) >= 1, 'error in right_group: ' + line

        assert SyntaxUnit.check_key(left_right[0]), 'error left: ' + line
        left = SyntaxUnit[left_right[0]]
        right = []
        for group in right_groups:
            assert group, line
            if group[0] in string.ascii_lowercase + string.ascii_uppercase:  # 非终结符
                assert SyntaxUnit.check_key(group), group + ' : ' + line  # 不在枚举类型中
                right.append(SyntaxUnit[group])

            else:  # 字符串 或者 正则表达式关键字
                assert SyntaxUnit.check_val(group), group + ' : ' + line  # 不在枚举类型的值中
                right.append(SyntaxUnit(group))

        production = Production(left, tuple(right))
        return production


class Grammar:
    def __init__(self, productions=None):
        if productions is None:
            productions = set()
        self.productions = productions

    def __str__(self):
        _str = ''
        for prod in self.productions:
            _str += str(prod) + '\n'
        return _str


def get_g_c_minus_auto() -> Grammar:
    grammar = Grammar(set())
    content = read_file('src/syntax/c_minus_grammar.txt')
    lines = content.split('\n')

    for line in lines:
        i = 0
        while line[i] in string.digits + '. ':  # 跳过序号
            i += 1
        line = line[i:]
        if line.endswith(';'):
            line = line[:-1]
        grammar.productions.add(Production.init_by_string(line))

    return grammar
