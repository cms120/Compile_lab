from collections import deque
from copy import deepcopy
from typing import Dict, Tuple, List, Set, Deque

from syntax.production import Production, is_terminal
from util import read_file, tuple_str, set_str


class Grammar:
    def __init__(self, s: str = 'program'):
        """
        :param s: 开始符号
        """
        self.__prods: Dict[str, Set[Tuple[str]]] = dict()
        self.__terminals: Set[str] = set()  # 终结符
        self.__non_terminals: Set[str] = set()  # 非终结符
        self.__s = s
        self.__first: Dict[Tuple[str], Set[str]] = dict()
        self.__follow: Dict[str, Set[str]] = dict()

    def __str__(self):
        res = ''
        for left, right in self.get_prods().items():
            res += left + ' ->'
            for r in right:
                res += ' ' + tuple_str(r)
            res += '\n'
        res += '\n'

        res += 'terminals: ' + set_str(self.__terminals) + '\n'
        res += 'non_terminals: ' + set_str(self.__non_terminals) + '\n'
        res += 's: ' + self.__s + '\n'

        res += 'first:\n'
        for i in self.__first.items():
            res += tuple_str(i[0]) + ' : ' + set_str(i[1]) + '\n'

        res += 'follow:\n'
        for i in self.__follow.items():
            res += i[0] + ' : ' + set_str(i[1]) + '\n'
        return res

    def add_prod(self, p: Production) -> None:
        """
        添加产生式
        """
        self.__prods[p.get_left()] = p.get_right()
        self.__non_terminals |= p.get_non_terminals()
        self.__terminals |= p.get_terminals()

    def add_prods(self, ps: List[Production]) -> None:
        for p in ps:
            self.add_prod(p)

    def get_prods(self) -> Dict[str, Set[Tuple[str]]]:
        return deepcopy(self.__prods)

    def get_terminals(self) -> Set[str]:
        return self.__terminals

    def get_s(self) -> str:
        return self.__s

    def get_r_first(self, r: Tuple[str]) -> Set[str]:
        """
        获得一个文法符号串的first集
        :returns: 如果符号串以非终结符起始直接返回第一个符号 否则查询first 有可能查询不到 即这个还未符号串的first集还未求出
        """
        if is_terminal(r[0]):
            return {r[0]}
        else:
            return self.__first.get(r, set())

    def get_chs_first(self, chs: Tuple[str]) -> Set[str]:
        """
        获得任意符号串的first集
        """
        res: Set[str] = set()
        for ch in chs:
            ch_first = self.get_ch_first(ch)
            assert len(ch_first) > 0, ch + ' ' + tuple_str(chs)
            res |= ch_first
            res.discard('$')  # 可能含有 $
            if '$' not in ch_first:  # 如果不含 $ 那么可以退出循环 否则继续向后
                return res
        res.add('$')  # 所有符号都含有 $ 那么可以加进first集

        return res

    def __set_r_first(self, r: Tuple[str]) -> bool:
        """
        得到一个符号串即产生式候选的first集 并赋值给first 有可能得不到
        :param r: 符号串
        :returns: 是否得到
        """
        r_first: Set[str] = set()

        for ch in r:
            ch_first = self.get_ch_first(ch)
            if len(ch_first) == 0:  # 该符号的first还求不出
                return False
            else:
                r_first |= ch_first
                r_first.discard('$')  # 可能含有 $
                if '$' not in ch_first:  # 如果不含 $ 那么可以退出循环 否则继续向后
                    self.__first[r] = r_first
                    return True
        r_first.add('$')  # 所有符号都含有 $ 那么可以加进first集
        self.__first[r] = r_first
        return True

    def get_ch_first(self, ch: str) -> Set[str]:
        """
        获得一个符号的first集
        :param ch: 符号
        :returns: first集 有可能是空集
        """
        if is_terminal(ch):
            return {ch}
        else:
            res: Set[str] = set()
            for r in self.__prods[ch]:  # 遍历产生式候选

                r_first = self.get_r_first(r)
                if len(r_first) == 0:  # 该产生式候选的first还未求出
                    return set()
                else:
                    res |= r_first
            return res

    def set_first(self):
        """
        文法的first集
        """
        r_live: Deque[Tuple[str]] = deque()  # 待设置first的符号串
        for left, right in self.get_prods().items():
            for r in right:  # 遍历产生式候选
                if not is_terminal(r[0]):
                    if not self.__set_r_first(r):
                        r_live.append(r)

        while len(r_live) > 0:  # 循环求first集
            r_now = r_live.pop()
            if not self.__set_r_first(r_now):
                r_live.appendleft(r_now)

    def check_first(self) -> bool:
        """
        LL1判断first是否相交
        """
        for left, right in self.__prods.items():
            r_first_set: Set[str] = set()
            r_first_set.add('¥')  # 人命币符号肯定不存在
            for r in right:
                r_first = self.get_r_first(r)
                if len(r_first_set & r_first) != 0:  # 有交集出错
                    return False
                else:
                    r_first_set |= r_first
        return True

    def init_follow(self):  # 初始化follow集
        for non_terminal in self.__non_terminals:
            self.__follow[non_terminal] = set()
        self.__follow[self.get_s()].add('#')

    def is_any_follow_grow(self):
        flag = False
        prods = self.get_prods()
        for left in prods.keys():
            rights = prods.get(left)  # rights:Set[tuple[str]]
            for right in rights:  # 遍历每一条规则
                for i in range(len(right) - 1):
                    if right[i] in self.__non_terminals:
                        self.__follow[right[i]] += self.__first[right[i]]
                        flag = True
                if right[-1] in self.__non_terminals:
                    self.__follow[right[-1]] += self.__follow[left]
                    flag = True
                if right[-1] in self.__non_terminals and '$' in self.__first[right[-1]] and len(right) > 1 and right[
                    -2] in self.__non_terminals:
                    self.__follow[right[-2]] += self.__follow[left]
                    flag = True
        return flag

    def set_follow(self):  # TODO 获得一个文法的follow集
        self.init_follow()
        while self.is_any_follow_grow:
            continue

    def init_by_lines(self, lines: List[str]) -> None:
        """
        通过多行程序来构造语法
        ['R -> S 'a' | 'a''
        ]
        """
        for line in lines:
            p = Production.init_by_line(line)
            self.add_prod(p)


def get_grammar_c_minus() -> Grammar:
    """
    构造c--的语法
    """
    g = Grammar()
    grammar_file = 'resource/更改文件/grammar2.txt'
    g.init_by_lines(read_file(grammar_file))
    return g
