import string
from copy import deepcopy
from typing import Set, List, Tuple, Dict

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


def get_new_tuple(t: Tuple[str], non_terminals: Set[str]):  # 只能满足一个tuple出现一对括号 待做
    new_list = list(t)
    left_index = new_list.index('(')
    right_index = new_list.index(')')
    if new_list[right_index + 1] == '*':
        left = ''
        right = set()
        temp_list = new_list[left_index:right_index + 1:1]

        for s in new_list[left_index + 1:right_index:1]:  # 构造left
            left += s
        left += '*'
        left = get_new_non_terminal(non_terminals, left)
        for i in range(left_index, right_index + 2):  # 将原tuple要替换的内容pop
            new_list.pop(left_index)
        new_list.insert(left_index, left)
        new_tuple = tuple(new_list)
        temp_list.append(left)
        right.add(tuple(temp_list))
        right.add(tuple('$'))

    elif new_list[right_index + 1] == '?':
        left = ''
        right = set()
        right.add(tuple(new_list[left_index + 1:right_index:1]))
        right.add(tuple('$'))

        for s in new_list[left_index + 1:right_index:1]:  # 构造left
            left += s
        left += '?'
        left = get_new_non_terminal(non_terminals, left)
        for i in range(left_index, right_index + 2):  # 将原tuple要替换的内容pop
            new_list.pop(left_index)
        new_list.insert(left_index, left)
        new_tuple = tuple(new_list)

    else:
        left = ''
        right = split_list(tuple(new_list[left_index + 1:right_index:1]))
        for s in new_list[left_index + 1:right_index:1]:  # 构造left
            left += s
        left = get_new_non_terminal(non_terminals, left)
        for i in range(left_index, right_index + 1):  # 将原tuple要替换的内容pop
            new_list.pop(left_index)
        new_list.insert(left_index, left)
        new_tuple = tuple(new_list)

    p = Production(left, right)
    return new_tuple, p


def dont_have_regex_symbol(right):  # 判断是否有必要继续递归
    for ch in ['(', ')', '|', '*', '?']:
        for t in right:
            if ch in t:
                return False
    return True


class Production:
    def __init__(self, left: str, right=None):
        if right is None:
            right = set()

        self.__left = left
        self.__right: Set[Tuple[str]] = set()
        self.__first: Dict[Tuple[str], str] = dict()  # 用于消除回溯 存储每个产生式候选的第一个字符 包括非终结符
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

        self.__first[r] = r[0]
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

    def if_direct_left_recursion(self) -> bool:
        """
        检查一条产生式是否有直接左递归
        """
        for r in self.__right:
            if r[0] == self.__left:
                return True
        return False

    @staticmethod
    def split_list_of_tuple(left: str, right: Set[Tuple[str]], non_terminals: Set[str]):
        # 判断结束递归调用
        if dont_have_regex_symbol(right):
            return [Production(left, right)]

        production_list = []

        new_right: Set[Tuple[str]] = set()  # right处理过的tuple的集合
        for t in right:  # 遍历当前处理过外部'|'的右部

            if '(' not in t:  # 不用处理的tuple
                new_right.add(t)
            else:
                new_tuple, p = get_new_tuple(t, non_terminals)  # 从要处理的tuple中得到new_tuple以及新生成的production
                production_list.append(p)
                new_right.add(new_tuple)

        production_list.append(Production(left, new_right))  # 将更新后的最初的的production加入到production_list中

        res = []  # 递归
        for p in production_list:
            res += Production.split_list_of_tuple(p.__left, p.__right, non_terminals)
        return res

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
        assert len(left_and_right) == 2, 'error left_and_right: ' + line

        right_with_or = left_and_right[1].split(' ')  # 分割字符串得到右边部分
        assert len(right_with_or) >= 1, 'error in right_group: ' + line

        return Production(left_and_right[0], set(split_list(tuple(right_with_or))))

    def remove_direct_left_recursion(self, non_terminals: Set[str]) -> List:
        """
        消除一个产生式的直接左递归

        P -> Pa1 | Pa2 | b1 | b2

        P -> b1P' | b2P'
        P' -> a1P' | a2P'
        :returns: 新的两个产生式

        """
        new_non_terminal = get_new_non_terminal(non_terminals, self.__left)

        res: List[Production] = [Production(self.__left),
                                 Production(new_non_terminal)]

        for r in self.__right:
            if r[0] == self.__left:  # 以P起始
                assert len(r) > 1, self  # 以P起始 那么后面必定还有值 不会 P->P
                new_r: List[str] = list(r[1:]) + [new_non_terminal]
                res[1].add_r(tuple(new_r))
            else:
                new_r: List[str] = []
                if r != '$':
                    new_r += r
                new_r.append(new_non_terminal)
                res[0].add_r(tuple(new_r))

        res[1].add_r(tuple(['$']))
        return res

    def check_first(self) -> bool:
        """
        检查一个产生式的候选 first集是否相交
        """
        return len(set(self.__first.values())) != len(self.__first.keys())

    def remove_recall(self, non_terminals: Set[str]) -> List:
        """
        消除回溯 返回若干产生式 提取左因子

        :returns: 两个新的产生式
        """
        if not self.check_first():  # 没有回溯
            return [self]

        left_factor = ''  # 相同左因子
        ch_set: Set[str] = set()
        for ch in self.__first.values():  # 遍历values 查找左因子
            if ch in ch_set:
                left_factor = ch
                break
            else:
                ch_set.add(ch)

        new_non_terminal = get_new_non_terminal(non_terminals, self.__left)
        res = [Production(self.__left), Production(new_non_terminal)]
        res[0].add_r(tuple([left_factor, new_non_terminal]))

        for r in self.get_right():
            if r[0] == left_factor:
                if len(r) == 1:  # 提取左因子后为空 即该产生式右侧只有一个左因子
                    res[1].add_r(tuple(['$']))
                else:
                    res[1].add_r(r[1:])
            else:
                res[0].add_r(r)

        return res[0].remove_recall(non_terminals) + res[1].remove_recall(non_terminals)  # 递归调用消除所有递归
