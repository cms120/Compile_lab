from lexical.token import Token
from syntax.grammar import get_grammar_c_minus
from syntax.syntax_tree import SyntaxTree, SyntaxTreeNode


def analysis_without_back(tokens: list[Token]) -> SyntaxTree:  # TODO
    g = get_grammar_c_minus()
    g.set_first()
    g.set_follow()

    tree = SyntaxTree(SyntaxTreeNode(g.get_s()))

    return tree
