import string
from typing import Dict, Tuple, List, Set

from src.util import read_file, spilt_list


class Grammar:
    def __init__(self, s: str = 'Program'):
        """
        :param s: 开始符号
        """
        self.productions: Dict[str, Set[Tuple[str]]] = dict()
        self.terminals: Set[str] = set()
        self.non_terminals: Set[str] = set()
        self.s = s

    def add_production_without_or(self, production: Tuple[str, Tuple[str]]) -> None:
        """
        :param production: 一条去除了 | 的产生式
        """
        if self.productions.get(production[0]) is None:
            self.productions[production[0]] = {production[1]}
        else:
            self.productions[production[0]].add(production[1])

    def add_production_with_or(self, production: Tuple[str, List[Tuple[str]]]) -> None:
        """
        :param production: 未去除 | 的产生式
        """
        for right_without_or in production[1]:
            self.add_production_without_or((production[0], right_without_or))

    def __str__(self):
        res = ''
        for left, right in self.productions.items():
            res += left + ' ->'
            for r in right:
                res += ' ' + str(r)
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

    @staticmethod
    def get_production_by_line(line: str) -> Tuple[str, List[Tuple[str]]]:
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

        return left_and_right[0], spilt_list(tuple(right_with_or))

    def get_first(self) -> dict:  # TODO 获得一个文法的first集
        pass

    def get_follow(self) -> dict:  # TODO 获得一个文法的follow集
        pass

    def init_by_lines(self, lines: List[str]) -> None:
        """
        通过多行程序来构造语法
        """
        for line in lines:
            production = Grammar.get_production_by_line(line)
            self.add_production_with_or(production)
            self.non_terminals.add(production[0])
            for r in production[1]:
                for ch in r:
                    if ch.startswith('\'') and ch.endswith('\''):
                        self.terminals.add(ch)
                    else:
                        self.non_terminals.add(ch)


def get_grammar_c_minus() -> Grammar:
    """
    构造c--的语法
    """
    g = Grammar()
    c_minus_grammar_file = 'src/syntax/c_minus_grammar.txt'
    g.init_by_lines(read_file(c_minus_grammar_file))
    return g
