import string
from typing import Dict, Tuple, List, Set

from src.util import read_file, spilt_list, tuple_str


class Production:
    def __init__(self, left: str, right: Set[Tuple[str]]):
        self.left = left
        self.right = right
        self.first: Dict[tuple[str], str] = dict()

    def __str__(self):
        res = self.left + '-> '

        for r in self.right:
            res += tuple_str(r) + ' '
        res += '\n'
        return res

    def if_direct_left_recursion(self) -> bool:
        """
        检查一条产生式是否有直接左递归
        """
        for r in self.right:
            if r[0] == self.left:
                return True
        return False

    @staticmethod
    def init_by_line(line: str) -> List:
        """
        根据一行grammar得到key和val

        :param line: 1. Program -> compUnit;
        :returns: (Program,(compUnit))
        """
        i = 0
        while line[i] in string.digits + '. ':  # 跳过序号
            i += 1
        line = line[i:]

        if line.endswith(';'):  # 去除结尾的分号
            line = line[:-1]
        # 去除后的效果 Program -> compUnit

        left_and_right = line.split(' -> ')
        assert len(left_and_right) == 2, 'error left_and_right: ' + line

        right_with_or = left_and_right[1].split(' ')
        assert len(right_with_or) >= 1, 'error in right_group: ' + line

        right_without_or = set(spilt_list(tuple(right_with_or)))

        p = Production(left_and_right[0], right_without_or)

        return p

    def remove_direct_left_recursion(self) -> List:
        """
        消除一个产生式的直接左递归

        P -> Pa1 | Pa2 | b1 | b2

        P -> b1P' | b2P'
        P' -> a1P' | a2P'
        :returns: 新的两个产生式


        """
        res: List[Production] = [Production(self.left, set()), Production(self.left + '\'', set())]

        for r in self.right:
            if r[0] == self.left:  # 以P起始
                new_right = tuple(list(r[1:]) + [self.left + '\''])

                res[1].right.add(new_right)
            else:
                new_right = tuple(list(r) + [self.left + '\''])
                res[0].right.add(new_right)

        res[1].right.add(tuple(['\'$\'']))
        return res

    def set_first(self):
        """
        获得一个产生式的First集
        """

        for r in self.right:  # 遍历产生式的每个候选
            self.first[r] = r[0]

    def check_first(self) -> bool:
        """
        检查一个产生式的候选 first集是否相交
        """

        return len(set(self.first.values())) != len(self.first.keys())


class Grammar:
    def __init__(self, s: str = 'Program'):
        """
        :param s: 开始符号
        """
        self.productions: Dict[str, Set[Tuple[str]]] = dict()
        self.terminals: Set[str] = set()  # 终结符
        self.non_terminals: Set[str] = set()  # 非终结符
        self.s = s
        self.first: Dict[str, Dict[Tuple[str], str]] = dict()
        self.follow = dict()

    def __str__(self):
        res = ''
        for left, right in self.productions.items():
            res += left + ' -> '
            for r in right:
                res += tuple_str(r) + ' '
            res += '\n'
        res += '\n'

        res += 'terminals:'
        for t in self.terminals:
            res += ' ' + t
        res += '\nnon_terminals:'
        for nt in self.non_terminals:
            res += ' ' + nt
        res += '\n'

        res += 's: ' + self.s + '\n'
        return res

    def add_production(self, p: Production) -> None:
        """
        添加产生式
        """
        self.productions[p.left] = p.right

        self.non_terminals.add(p.left)
        for r in p.right:
            for str_r in r:
                if str_r.startswith('\'') and str_r.endswith('\''):
                    self.terminals.add(str_r)
                else:
                    self.non_terminals.add(str_r)

    def set_first(self):  # TODO 获得一个文法的first集
        pass

    def set_follow(self):  # TODO 获得一个文法的follow集
        pass

    def init_by_lines(self, lines: List[str]) -> None:
        """
        通过多行程序来构造语法
        ['R -> S 'a' | 'a''
        ]
        """
        for line in lines:
            production = Production.init_by_line(line)
            self.add_production(production)


def get_grammar_c_minus() -> Grammar:
    """
    构造c--的语法
    """
    g = Grammar()
    c_minus_grammar_file = 'src/syntax/c_minus_grammar.txt'
    g.init_by_lines(read_file(c_minus_grammar_file))
    return g
