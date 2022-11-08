import os.path

from graphviz import Digraph

import util
from lexical.dfa import DFA
from lexical.fa import FA
from syntax.grammar import Grammar


def graph_fa_print(fa: FA, file_name='FA'):  # 画NFA的图像

    g = Digraph(comment='graph_fa')
    for f in fa.f.items():  # 遍历转换函数
        for val in f[1]:
            g.edge(f[0][0], val, f[0][1])

    g.node(fa.s, color='red')  # 开始节点红色
    for z in fa.z:
        g.node(z, shape='doublecircle')  # 结束节点双层

    g.render( file_name + '.gv', view=True)


def graph_dfa_print(dfa: DFA, file_name='DFA'):
    fa_f = dict()
    for item in dfa.f.items():
        fa_f[item[0]] = {item[1]}

    fa = FA(dfa.k, dfa.letters, fa_f, dfa.s, dfa.z)
    graph_fa_print(fa, file_name)


def graph_grammar(g: Grammar, file_name='grammar'):
    graph = Digraph(comment='graph_grammar')
    for prod in g.get_prods().items():
        for val in prod[1]:
            graph.edge(prod[0], util.tuple_str(val)[2:-2])  # 去除结尾和开头的括号

    graph.node(g.get_s(), color='red')
    for ter in g.get_terminals():
        graph.node(ter, shape='doublecircle')

    graph.render(os.path.join('result/grammar', file_name + '.gv'), view=True)
