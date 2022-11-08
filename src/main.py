import lexical.lexical_analysis as la
import syntax_top_down.ll1 as ll
from lexical.token import tokens_to_deque
from util import write_file

res_file = 'result/syntax/analysis.txt'
tokens = la.analysis('resource/change_file/源文件/01_var_defn.sy')
states = ll.analysis(tokens)


