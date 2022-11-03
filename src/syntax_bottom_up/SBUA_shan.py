from collections import deque
from typing import List, Set, Tuple, Deque

from src.lexical.token import Token
from src.syntax.grammar import Grammar, Production
from src.syntax.syntax_tree import SyntaxTree, SyntaxTreeNode


def remove_recall(g: Grammar):
    """
    消除一个文法的回溯 通过不断地提取左因子
    """
    non_ter_list = list(g.non_terminals)
    for non_ter in non_ter_list:
        p = Production(non_ter, g.productions[non_ter])
        for p_new in p.remove_recall(g.non_terminals):
            g.add_production(p_new)


def remove_left_recursion_simple(g: Grammar):
    """
    化简消除左递归后的文法
    """
    stack_non_terminals: Deque[str] = deque()  # 待访问非终结符
    stack_non_terminals.append(g.s)  # 以g的起始符号开始
    new_non_terminals = set()

    while len(stack_non_terminals) != 0:
        now = stack_non_terminals.pop()
        new_non_terminals.add(now)

        for r in g.productions[now]:  # 遍历产生式
            for ch in r:  # 遍历符号
                if ch in g.non_terminals and ch not in new_non_terminals:  # 是非终结符且未被访问过
                    stack_non_terminals.append(ch)

    del_non_terminals = g.non_terminals - new_non_terminals  # 待去除的非终结符
    g.non_terminals = new_non_terminals
    for ch in del_non_terminals:
        del g.productions[ch]


def remove_direct_left_recursion_single(g: Grammar, p_i: str):
    """
    消除一个文法的一个非终结符的直接左递归

    :param g: 文法
    :param p_i: 非终结符
    """

    p = Production(p_i, g.productions[p_i])
    if p.if_direct_left_recursion():
        ps = p.remove_direct_left_recursion(g.non_terminals)
        for p_new in ps:
            g.add_production(p_new)


def remove_left_recursion_single(g: Grammar, p_i: str, p_j: str):
    """
    根据 p_i p_j 消除左递归
    """
    new_right: Set[Tuple[str]] = set()
    for r in g.productions[p_i]:  # 遍历 Pi 的每一个产生式
        if r[0] == p_j:  # Pi -> Pj a
            for j_r in g.productions[p_j]:  # 遍历 Pj 的每一个产生式
                new_right.add(tuple(j_r + r[1:]))

        else:
            new_right.add(r)
    g.productions[p_i] = new_right


def remove_left_recursion(g: Grammar):
    """
    消除左递归
    """

    non_terminals: List[str] = list(g.non_terminals)
    for i in range(len(non_terminals)):
        for j in range(i):
            remove_left_recursion_single(g, non_terminals[i], non_terminals[j])

        remove_direct_left_recursion_single(g, non_terminals[i])

    remove_left_recursion_simple(g)


def analysis_without_back(g: Grammar, tokens: list[Token]) -> SyntaxTree:  # TODO
    remove_left_recursion(g)
    remove_recall(g)

    tree = SyntaxTree(SyntaxTreeNode(g.s))

    return tree
