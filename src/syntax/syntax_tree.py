from collections import deque

from src.syntax.syntax_unit import SyntaxUnit


class SyntaxTreeNode:  # 书中的一个节点
    def __init__(self, su: SyntaxUnit):
        self.su = su
        self.children = deque()

    def add_child(self, child) -> None:
        self.children.append(child)


class SyntaxTree:
    def __init__(self, s):
        self.s = s
