import src.lexical.lexical_analysis as la
from src.lexical.token import Token
from src.syntax.grammar import Grammar, get_g_c_minus_auto
from src.syntax.syntax_tree import SyntaxTree, SyntaxTreeNode
from src.syntax.syntax_unit import SyntaxUnit


# 根据文法来分析token list


def analysis() -> SyntaxTree:  # c--的语法分析
    return analysis_with_back(get_g_c_minus_auto(),
                              la.analysis())


def analysis_with_back(g: Grammar, tokens: list[Token]) -> SyntaxTree:  # 带有回溯的分析一个token list TODO 不能含有左递归
    s_node = SyntaxTreeNode(SyntaxUnit.Program)
    tree = SyntaxTree(s_node)

    token_p = 0  # token指针
    while token_p != len(tokens):
        pass

    return tree


def analysis_without_back(g: Grammar, tokens: list[Token]) -> SyntaxTree:  # TODO
    s_node = SyntaxTreeNode(SyntaxUnit.Program)
    tree = SyntaxTree(s_node)

    return tree
