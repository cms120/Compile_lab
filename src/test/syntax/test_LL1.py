
import string
import sys
sys.path.append('D:/Complie/compile_lab')
from src.syntax_bottom_up.syntax_bottom_up_analysis import GrammartextTodict,getnoOrList,DisDirectRecursionToDirect,remove_direct_left_recursion,twoListTodict,simplified
from src.syntax.grammar import Grammar, Production, get_g_c_minus_auto
from src.syntax.syntax_unit import SyntaxUnit
from src.syntax.syntax_tree import SyntaxTree


listvalueNoor= getnoOrList(GrammartextTodict().values())
listkey = list(GrammartextTodict().keys())

Direct_list_no_key = DisDirectRecursionToDirect(listkey,listvalueNoor)

tuplee =remove_direct_left_recursion(listkey,Direct_list_no_key)

dictre = twoListTodict(tuplee[0],tuplee[1])

dictresult = simplified(dictre)

print(dictresult)

# d = {'R':['S','a','|','a'],'Q':['R','b','|','b'],'S':['Q','c','|','c']}

# listvalueNoor=getnoOrList(d.values())
# listkey = list(d.keys())

# Direct_list_no_key = DisDirectRecursionToDirect(listkey,listvalueNoor)

# tuplee =remove_direct_left_recursion(listkey,Direct_list_no_key)

# dictre = twoListTodict(tuplee[0],tuplee[1])

# dictresult = simplified(dictre)

# print(dictresult)
