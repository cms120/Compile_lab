import string
from collections import deque

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

    def check_left_recursion(self) -> bool:  # TODO 检查是否有左递归
        pass

    @staticmethod
    def get_units_list_by_str(line: str) -> list[SyntaxUnit]:  # 一行字符串拆分为若干 unit
        left_right = line.split(' -> ')
        assert len(left_right) == 2, 'error left_right: ' + line

        right_groups = left_right[1].split(' ')
        assert len(right_groups) >= 1, 'error in right_group: ' + line
        assert SyntaxUnit.check_key(left_right[0]), 'error left: ' + line

        units = [SyntaxUnit[left_right[0]]]

        right_with_op = []  # 带有 |  的产生式右端
        for group in right_groups:
            assert group, line
            if group[0] in string.ascii_lowercase + string.ascii_uppercase:  # 非终结符
                assert SyntaxUnit.check_key(group), group + ' : ' + line  # 不在枚举类型中
                right_with_op.append(SyntaxUnit[group])

            else:  # 字符串 或者 正则表达式关键字
                assert SyntaxUnit.check_val(group), group + ' : ' + line  # 不在枚举类型的值中
                right_with_op.append(SyntaxUnit(group))

        return units + right_with_op

    @staticmethod
    def init_list_by_units(units: list[SyntaxUnit]):  # 通过 units 构建产生式
        return Production(units[0], tuple(units[1:]))

    @staticmethod
    def divide_by_or_op(right) -> list[list[SyntaxUnit]]:  # 将产生式右端根据 | 拆分 这里 | 不能出现在开始和结束
        # 暂时没用
        indexes = []  # | 的索引
        rights = []
        l_par = 0
        for i in range(len(right)):
            if right[i] == SyntaxUnit('|'):
                if l_par == 0:  # 不在括号中
                    indexes.append(i)
            if right[i] == SyntaxUnit('('):
                l_par += 1

            if right[i] == SyntaxUnit(')'):
                l_par -= 1
        if len(indexes) == 0:
            rights = [right]
        else:
            rights.append(right[:indexes[0]])
            for i in range(len(indexes) - 1):
                rights.append(right[indexes[i] + 1:indexes[i + 1]])
            rights.append(right[indexes[-1] + 1:])

        return rights


class Grammar:
    def __init__(self, productions=None):
        if productions is None:
            productions = deque()
        self.productions = productions

    def __str__(self):
        _str = ''
        for prod in self.productions:
            _str += str(prod) + '\n'
        return _str


def get_g_c_minus_auto() -> Grammar:
    grammar = Grammar()
    content = read_file('src/syntax/c_minus_grammar.txt')
    lines = content.split('\n')

    for line in lines:
        i = 0
        while line[i] in string.digits + '. ':  # 跳过序号
            i += 1
        line = line[i:]
        if line.endswith(';'):
            line = line[:-1]

        units = Production.get_units_list_by_str(line)
        grammar.productions.append(Production.init_list_by_units(units))
    return grammar
