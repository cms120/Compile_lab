from typing import List, Set, Tuple

from src.lexical.token import Token
from src.syntax.grammar import Grammar, Production
from src.syntax.syntax_tree import SyntaxTree, SyntaxTreeNode


def remove_recall(g: Grammar):
    pass


def remove_direct_left_recursion(g: Grammar):
    """
    消除一个文法的直接左递归
    """
    new_p: List[Production] = []
    for item in g.productions.items():
        p = Production(item[0], item[1])
        if p.if_direct_left_recursion():
            ps = p.remove_direct_left_recursion()
            new_p += ps

    for p in new_p:
        g.add_production(p)


def remove_left_recursion_single(g: Grammar, i: int, j: int, non_terminals: List[str]):
    """
    根据 i j 消除左递归
    """
    new_right: Set[Tuple[str]] = set()
    for r in g.productions[non_terminals[i]]:  # 遍历 Pi 的每一个产生式
        if r[0] == non_terminals[j]:  # Pi -> Pj a
            new_r = set()
            for j_r in g.productions.get(non_terminals[j]):  # 遍历 Pj 的每一个产生式
                new_r.add(tuple(j_r + r[1:]))
            new_right += new_r
        else:
            new_right.add(r)
    g.productions[non_terminals[i]] = new_right


def remove_left_recursion(g: Grammar):
    """
    消除左递归
    """
    remove_direct_left_recursion(g)  # 先消除直接左递归

    non_terminals: List[str] = list(g.non_terminals)
    for i in range(len(non_terminals)):
        for j in range(i):

            remove_left_recursion_single(g, i, j, non_terminals)


def analysis_without_back(g: Grammar, tokens: list[Token]) -> SyntaxTree:  # TODO
    remove_left_recursion(g)
    remove_recall(g)

    tree = SyntaxTree(SyntaxTreeNode(g.s))

    return tree
