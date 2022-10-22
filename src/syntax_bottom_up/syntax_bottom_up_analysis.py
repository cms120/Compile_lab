from src.lexical.token import Token
from src.syntax.grammar import Grammar


class SyntaxBottomUpAnalysis:  # 根据文法来分析token list
    def __init__(self, g: Grammar):
        self.g = g

    def analysis_with_back(self, tokens: list[Token]):  # 带有回溯的分析一个token list
        pass


