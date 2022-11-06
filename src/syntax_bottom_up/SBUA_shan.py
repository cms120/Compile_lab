from collections import deque
from typing import List, Deque

from lexical.token import Token
from syntax.grammar import Grammar, Production
from syntax.syntax_tree import SyntaxTree, SyntaxTreeNode


def remove_recall(g: Grammar):
    """
    消除一个文法的回溯 通过不断地提取左因子
    """
    non_ter_list = list(g.get_non_terminals())
    for non_ter in non_ter_list:
        p = Production(non_ter, g.get_prods()[non_ter])
        g.add_prods(p.remove_recall(g.get_non_terminals()))


def remove_left_recursion_simple(g: Grammar):
    """
    化简消除左递归后的文法
    """
    stack_non_terminals: Deque[str] = deque()  # 待访问非终结符
    stack_non_terminals.append(g.get_s())  # 以g的起始符号开始
    new_non_terminals = set()

    while len(stack_non_terminals) != 0:
        now = stack_non_terminals.pop()
        new_non_terminals.add(now)

        for r in g.get_prods()[now]:  # 遍历产生式
            for ch in r:  # 遍历符号
                if ch in g.get_non_terminals() and ch not in new_non_terminals:  # 是非终结符且未被访问过
                    stack_non_terminals.append(ch)

    del_non_terminals = g.get_non_terminals() - new_non_terminals  # 待去除的非终结符
    g.del_prods(del_non_terminals)


def remove_direct_left_recursion_single(g: Grammar, p_i: str):
    """
    消除一个文法的一个非终结符的直接左递归

    :param g: 文法
    :param p_i: 非终结符
    """

    p = Production(p_i, g.get_prods()[p_i])
    if p.if_direct_left_recursion():
        ps = p.remove_direct_left_recursion(g.get_non_terminals())
        g.add_prods(ps)


def remove_left_recursion_single(g: Grammar, p_i: str, p_j: str):
    """
    根据 p_i p_j 消除左递归
    """
    j_right = g.get_prods()[p_j]
    p = Production(p_i)

    for r in g.get_prods()[p_i]:  # 遍历 Pi 的每一个产生式
        if r[0] == p_j:  # Pi -> Pj a, a有可能为空
            for j_r in j_right:  # 遍历 Pj 的每一个产生式
                new_r: List[str] = []
                if j_r != tuple(['$']):  # 如果 j_r 是$那么不添加 因为r有可能不为$
                    new_r += list(j_r)
                if len(r) > 1:  # r的长度大于1 即a不为空
                    new_r += r[1:]
                if len(new_r) == 0:
                    new_r.append('$')  # 此时新地产生式还为空
                p.add_r(tuple(new_r))
        else:
            p.add_r(r)
    g.add_prod(p)


def remove_left_recursion(g: Grammar):
    """
    消除左递归
    """

    non_terminals: List[str] = list(g.get_non_terminals())
    for i in range(len(non_terminals)):
        for j in range(i):
            remove_left_recursion_single(g, non_terminals[i], non_terminals[j])

        remove_direct_left_recursion_single(g, non_terminals[i])

    remove_left_recursion_simple(g)


def analysis_without_back(g: Grammar, tokens: list[Token]) -> SyntaxTree:  # TODO
    remove_left_recursion(g)
    remove_recall(g)

    tree = SyntaxTree(SyntaxTreeNode(g.get_s()))

    return tree
