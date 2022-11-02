from collections import deque


class SyntaxTreeNode:  # 书中的一个节点
    def __init__(self, su: str):
        self.su = su
        self.children = deque()

    def add_child(self, child) -> None:
        self.children.append(child)


class SyntaxTree:
    def __init__(self, s):
        self.s = s
