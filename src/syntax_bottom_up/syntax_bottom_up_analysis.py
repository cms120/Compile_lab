import src.lexical.lexical_analysis as la
from src.lexical.token import Token
from src.syntax.grammar import Grammar, get_g_c_minus_auto


# 根据文法来分析token list


def analysis():  # c--的语法分析
    analysis_with_back(get_g_c_minus_auto(),
                       la.analysis())


def analysis_with_back(g: Grammar, tokens: list[Token]):  # 带有回溯的分析一个token list TODO

    pass


def analysis_without_back(g: Grammar, tokens: list[Token]):  # TODO
    pass
