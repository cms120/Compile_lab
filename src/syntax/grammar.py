import string
from typing import Dict, Tuple, List, Set

from src.util import read_file, split_list, tuple_str


def get_new_non_terminal(non_terminals: Set[str], now: str) -> str:
    """
    传入已有的非终结符 得到一个新的非终结符
    """
    res = now
    while res in non_terminals:
        res += '\''
    return res


def get_new_tuple(t: Tuple[str], non_terminals: Set[str]):  # 只能满足一个tuple出现一对括号 待做
    new_list = list(t)
    left_index = new_list.index('(')
    right_index = new_list.index(')')
    if new_list[right_index + 1] == '*':
        left = ''
        new_list.pop(left_index)
        new_list.pop(right_index)
        new_list.pop(right_index + 1)
        new_tuple = tuple(new_list)

        for s in list[left_index + 1:right_index:1]:
            left += s
        right = set()
        right.add(tuple(left))
        right.add(tuple('$'))

    elif new_list[right_index + 1] == '?':
        left = ''
        new_list.pop(left_index)
        new_list.pop(right_index)
        new_list.pop(right_index + 1)
        new_tuple = tuple(new_list)

        for s in list[left_index + 1:right_index:1]:
            left += s
        right = set()
        right.add(tuple(list[left_index + 1:right_index:1]))
        right.add(tuple('$'))
    else:
        left = ''
        new_list.pop(left_index)
        new_list.pop(right_index)
        new_tuple = tuple(new_list)

        for s in list[left_index + 1:right_index:1]:
            left += s
        right = set(split_list(tuple(list[left_index + 1:right_index:1])))

    p = Production(get_new_non_terminal(non_terminals, left), right)
    return new_tuple, p


def dont_have_regex_symbol(right):  # 判断是否有必要继续递归
    for ch in ['(', ')', '|', '*', '?']:
        for t in right:
            if ch in t:
                return False
    return True


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
    def split_list_of_tuple(left: str, right: Set[Tuple[str]], non_terminals: Set[str]):
        # 判断结束递归调用
        if dont_have_regex_symbol(right):
            return Production(left, right)

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
            res += Production.split_list_of_tuple(p.left, p.right, non_terminals)
        return res

    @staticmethod
    def init_by_line(line: str, non_terminals: Set[str]) -> List:
        """
        根据一行grammar得到若干production

        :param line: 1. Program -> compUnit;
        :param non_terminals: 用于获得下一个非终结符
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

        right_without_outSides_brackets_or = set(split_list(tuple(right_with_or)))

        res = Production.split_list_of_tuple(left_and_right[0], right_without_outSides_brackets_or, non_terminals)

        return [res]

    def remove_direct_left_recursion(self, non_terminals: Set[str]) -> List:
        """
        消除一个产生式的直接左递归

        P -> Pa1 | Pa2 | b1 | b2

        P -> b1P' | b2P'
        P' -> a1P' | a2P'
        :returns: 新的两个产生式


        """
        res: List[Production] = [Production(self.left, set()), Production(self.left + '\'', set())]

        for r in self.right:
            new_non_terminal = get_new_non_terminal(non_terminals, self.left)
            if r[0] == self.left:  # 以P起始
                new_right = tuple(list(r[1:]) + [new_non_terminal])

                res[1].right.add(new_right)
            else:
                new_right = tuple(list(r) + [new_non_terminal])
                res[0].right.add(new_right)

        res[1].right.add(tuple(['\'$\'']))
        return res

    def set_first(self):
        """
        获得一个产生式的First集
        """
        # TODO 没有处理非终结符
        for r in self.right:  # 遍历产生式的每个候选
            self.first[r] = r[0]

    def check_first(self) -> bool:
        """
        检查一个产生式的候选 first集是否相交
        """

        return len(set(self.first.values())) != len(self.first.keys())

    def remove_recall(self, non_terminals: Set[str]) -> List:
        """
        消除回溯 返回若干产生式 提取左因子

        :returns: 两个新的产生式
        """
        self.set_first()
        if not self.check_first():  # 没有回溯
            return [self]

        left_factor = ''  # 相同左因子
        ch_set: Set[str] = set()
        for ch in self.first.values():  # 遍历values 查找左因子
            if ch in ch_set:
                left_factor = ch
                break
            else:
                ch_set.add(ch)

        new_non_terminal = get_new_non_terminal(non_terminals, self.left)
        res = [Production(self.left, set()), Production(new_non_terminal, set())]
        res[0].right.add(tuple([left_factor, new_non_terminal]))

        for r in self.right:
            if r[0] == left_factor:
                res[1].right.add(r[1:])
            else:
                res[0].right.add(r)

        return res[0].remove_recall(non_terminals) + res[1].remove_recall(non_terminals)  # 递归调用消除所有递归


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
            ps = Production.init_by_line(line, self.non_terminals)
            for p in ps:
                self.add_production(p)


def get_grammar_c_minus() -> Grammar:
    """
    构造c--的语法
    """
    g = Grammar()
    c_minus_grammar_file = 'src/syntax/c_minus_grammar.txt'
    g.init_by_lines(read_file(c_minus_grammar_file))
    return g
