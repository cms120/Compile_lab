import string
from typing import Dict, Tuple, List

from src.util import read_file


class Grammar:
    def __init__(self):
        self.productions: Dict[str, Tuple[str]] = dict()

    def add_production(self, production: Tuple[str, Tuple[str]]) -> None:
        self.productions[production[0]] = production[1]

    def __str__(self):
        s = ''
        for left, right in self.productions.items():
            s += left + ' ->'
            for r in right:
                s += ' ' + r
            s += '\n'
        return s

    @staticmethod
    def get_production_by_line(line: str) -> Tuple[str, Tuple[str]]:
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

        right_groups = left_and_right[1].split(' ')
        assert len(right_groups) >= 1, 'error in right_group: ' + line

        return left_and_right[0], tuple(right_groups)

    def get_first(self) -> dict:  # TODO 获得一个文法的first集
        pass

    def get_follow(self) -> dict:  # TODO 获得一个文法的follow集
        pass

    def init_by_file(self, file: str) -> None:
        """
        通过文件来构造语法
        """
        lines = read_file(file)
        for line in lines:
            self.add_production(Grammar.get_production_by_line(line))

    def init_c_minus(self) -> None:
        """
        构造c--的语法
        """
        self.init_by_file('src/syntax/c_minus_grammar.txt')

    @staticmethod
    def divide_by_or_op(right: Tuple[str]) -> List[Tuple[str]]:  # 暂时没用 将产生式右端根据 | 拆分 这里 | 不能出现在开始和结束
        indexes = []  # | 的索引
        rights: List[Tuple[str]] = []
        l_par = 0
        for i in range(len(right)):
            if right[i] == '|':
                if l_par == 0:  # 不在括号中
                    indexes.append(i)
            if right[i] == '(':
                l_par += 1

            if right[i] == ')':
                l_par -= 1
        if len(indexes) == 0:
            rights = [right]
        else:
            rights.append(right[:indexes[0]])
            for i in range(len(indexes) - 1):
                rights.append(right[indexes[i] + 1:indexes[i + 1]])
            rights.append(right[indexes[-1] + 1:])

        return rights
