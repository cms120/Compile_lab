import src.lexical.lexical_analysis as la
from src.lexical.token import Token
from src.syntax.grammar import Grammar, get_g_c_minus_auto
from src.syntax.syntax_tree import SyntaxTree, SyntaxTreeNode
from src.syntax.syntax_unit import SyntaxUnit


# 根据文法来分析token list


def check_left_recursion(g: Grammar) -> bool:  # 检查一个文法是否有左递归
    pass


def check_first(g: Grammar) -> bool:  # 检查一个文法的first集
    first_dict = g.get_first()
    pass


def check_follow(g: Grammar) -> bool:  # 检查一个文法的follow集
    follow_dict = g.get_follow()
    pass


def check_if_ll_one(g: Grammar) -> bool:  # 检查一个文法是否是ll(1)
    return check_follow(g) and check_first(g) and check_left_recursion(g)


def analysis() -> SyntaxTree:  # c--的语法分析
    return analysis_without_back(get_g_c_minus_auto(),
                                 la.analysis())


def remove_left_recursion(g: Grammar):  # TODO 消除一个文法的左递归
    return g


def remove_recall(g: Grammar):  # TODO 消除回溯
    return g


def analysis_with_back(g: Grammar, tokens: list[Token]) -> SyntaxTree:  # 带有回溯的分析一个token list TODO 不能含有左递归
    # 应该是没用了
    s_node = SyntaxTreeNode(SyntaxUnit.Program)
    tree = SyntaxTree(s_node)

    token_p = 0  # token指针
    while token_p != len(tokens):
        pass

    return tree


def analysis_without_back(g: Grammar, tokens: list[Token]) -> SyntaxTree:  # TODO
    remove_left_recursion(g)
    remove_recall(g)

    s_node = SyntaxTreeNode(SyntaxUnit.Program)
    tree = SyntaxTree(s_node)

    return tree
