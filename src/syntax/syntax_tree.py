from collections import deque
from typing import Deque


class SyntaxTreeNode:  # 树中的一个节点
    def __init__(self, su: str, is_s=False, is_leaf=False):
        self.__su = su
        self.__children: Deque[SyntaxTreeNode] = deque()
        self.__father: SyntaxTreeNode = SyntaxTreeNode('¥')
        self.__is_s = is_s
        self.__is_leaf: bool = is_leaf
        self.is_live = True

    def add_child(self, child) -> None:
        self.__children.append(child)

    def is_leaf(self) -> bool:
        return self.__is_leaf

    def get_fa(self):
        if not self.__is_s:
            return self.__father

    def get_first_child(self):
        return self.__children[0]

    def get_next_child(self, child_now):

        for i in range(len(self.__children)):
            if self.__children[i] == child_now:  # 找到这个孩子
                if i == len(self.__children) - 1:  # 是最后一个
                    return None
                else:
                    return self.__children[i + 1]
        assert False, self


class SyntaxTree:
    def __init__(self, s: SyntaxTreeNode):
        self.__s = s
        self.__node_now = s

    def get_next_node(self) -> SyntaxTreeNode:
        if not self.__node_now.is_leaf():  # 不是叶子 先找儿子
            self.__node_now = self.__node_now.get_first_child()
        else:  # 找右边的兄弟
            brother = self.__node_now
            if brother is None:  # 自己是最右边的
                self
