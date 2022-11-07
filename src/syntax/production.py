import string
from copy import deepcopy
from typing import Set, Tuple

from util import split_list, tuple_str


def is_terminal(ter: str) -> bool:
    return (ter.startswith("'") and ter.startswith("'")) or ter == '$'


def get_new_non_terminal(non_terminals: Set[str], now: str) -> str:
    """
    传入已有的非终结符 得到一个新的非终结符
    """
    res = now
    if res.startswith("'"):
        res = 'n' + res
    while res in non_terminals:
        res += "'"
    return res


class Production:
    def __init__(self, left: str, right=None):
        if right is None:
            right = set()

        self.__left = left
        self.__right: Set[Tuple[str]] = set()
        self.__non_terminals: Set[str] = {left}
        self.__terminals: Set[str] = set()

        self.add_right(right)

        assert not is_terminal(left), self

    def __str__(self):
        res = self.__left + '-> '

        for r in self.get_right():
            res += tuple_str(r) + ' '
        res += '\n'
        return res

    def add_r(self, r: Tuple[str]) -> None:
        """
        添加一个产生式候选 只能通过这个函数来添加
        :param r: 一个产生式候选
        """
        if len(r) > 1:
            assert '$' not in r, str(self) + '\nr: ' + tuple_str(r)
        for ch in r:
            if is_terminal(ch):
                self.__terminals.add(ch)
            else:
                self.__non_terminals.add(ch)

        self.__right.add(r)

    def add_right(self, right: Set[Tuple[str]]) -> None:
        for r in right:
            self.add_r(r)

    def get_left(self) -> str:
        return deepcopy(self.__left)

    def get_right(self) -> Set[Tuple[str]]:
        return deepcopy(self.__right)

    def get_non_terminals(self) -> Set[str]:
        return self.__non_terminals

    def get_terminals(self) -> Set[str]:
        return self.__terminals

    @staticmethod
    def init_by_line(line: str):
        """
        根据一行grammar得到若干production

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

        right_with_or = left_and_right[1].split(' ')  # 分割字符串得到右边部分

        return Production(left_and_right[0], set(split_list(tuple(right_with_or))))
