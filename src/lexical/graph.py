from graphviz import Digraph

from src.lexical.deterministic_finite_automation import DFA
from src.lexical.finite_automation import FA


class Graph:
    dfa_name = 1

    @staticmethod
    def graph_fa_print(fa: FA):  # 画NFA的图像

        g = Digraph('G', filename='DFA' + str(Graph.dfa_name) + '.gv', format='png')
        for f in fa.f.items():
            for val in f[1]:
                g.edge(f[0][0], val, f[0][1])

        g.node(fa.s, color='res')  # 开始节点红色
        for z in fa.z:
            g.node(z, shape='doublecircle')  # 结束节点双层

        Graph.dfa_name += 1

        g.view()

