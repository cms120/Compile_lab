from graphviz import Digraph

from src.lexical.deterministic_finite_automation import DFA
from src.lexical.finite_automation import FA


class Graph:
    dfa_name = 1

    @staticmethod
    def graph_dfa_print(dfa: DFA):  # 画NFA的图像

        g = Digraph('G', filename='DFA' + str(Graph.dfa_name) + '.gv', format='png')
        for f in dfa.f.items():
            g.edge(f[0][0], f[1], f[0][1])

        g.node(dfa.s, color='res')  # 开始节点红色
        for z in dfa.z:
            g.node(z, shape='doublecircle')  # 结束节点双层

        Graph.dfa_name += 1

        g.view()

    @staticmethod
    def graph_fa_print(fa: FA):
        f = dict()
        for item in fa.f.items():
            for val in item[1]:
                f[item[0]] = val

        Graph.graph_dfa_print(DFA(fa.k, fa.letters, f, fa.s, fa.z))
