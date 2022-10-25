from graphviz import Digraph

from src.lexical.deterministic_finite_automation import DFA
from src.lexical.finite_automation import FA


def graph_fa_print(fa: FA):  # 画NFA的图像

    g = Digraph(comment='graph_fa')
    for f in fa.f.items():  # 遍历转换函数
        for val in f[1]:
            g.edge(f[0][0], val, f[0][1])

    g.node(fa.s, color='res')  # 开始节点红色
    for z in fa.z:
        g.node(z, shape='doublecircle')  # 结束节点双层

    g.render('DFA.gv', view=True)


def graph_dfa_print(dfa: DFA):
    fa = FA(dfa.k, dfa.letters, dfa.f, dfa.s, dfa.z)
    graph_fa_print(fa)
