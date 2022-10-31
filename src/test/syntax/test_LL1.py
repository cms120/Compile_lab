
import sys
sys.path.append('D:/Complie/compile_lab')
from src.syntax.grammar import Grammar, Production, get_g_c_minus_auto
from src.syntax_bottom_up.syntax_bottom_up_analysis import remove_left_recursion, remove_recall
#以下为测试消除左递归：

# grammar = get_g_c_minus_auto()
# print(remove_left_recursion(grammar))


grammar = Grammar()
grammar_result = Grammar()
grammar_list = ['Q -> b | R b','R -> a | S a','S -> c | Q c']
#grammar_list = ['R -> a | S a','Q -> b | R b','S -> c | Q c']
# grammar_list = ['S -> c | Q c','R -> a | S a','Q -> b | R b']
# grammar_list = ['S -> c | Q c','Q -> b | R b','R -> a | S a']
# grammar_result_list = ['R -> \'const\' a | a','Q -> S a b | a b | b','S -> a b c Ss | b c Ss | c Ss','Ss -> a b c Ss | epsilon']

for s in grammar_list:
     grammar.productions.append(Production.init_by_str(s))

# for s in grammar_result_list:
#      grammar_result.productions.append(Production.init_by_str(s))


print(grammar)
# print(grammar_result)
print(remove_left_recursion(grammar))
# print(remove_left_recursion(grammar)==grammar)

# 以下为测试消除回溯：
# grammar2 = Grammar()
# grammar2_result = Grammar()
# grammar2_list = ['A -> a d | a A C | d d As']
# grammar2_result_list = ['A -> a F | d d As','F -> d | A C']

# for s in grammar2_list:
#      grammar2.productions.append(Production.init_by_str(s))

# for s in grammar2_result_list:
#      grammar2_result.productions.append(Production.init_by_str(s))

# print(grammar2)
# print(grammar2_result)
# print('消除回溯方法完成情况：',remove_recall(grammar) == grammar_result)

