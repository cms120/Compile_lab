from collections import deque

from lexical import lexical_analysis
from syntax_top_down import ll1

tokens = lexical_analysis.analysis('resource/change_file/源文件/04_var_defn.sy')
ll1.analysis(deque(tokens))
