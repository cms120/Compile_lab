import sys

sys.path.append('D:/Complie/compile_lab')
from syntax_bottom_up.syntax_bottom_up_analysis import grammar_text_to_dict, get_no_or_list, \
    DisDirectRecursionToDirect, remove_direct_left_recursion, two_list_to_dict, simplified

listvalueNoor = get_no_or_list(grammar_text_to_dict().values())
listkey = list(grammar_text_to_dict().keys())

Direct_list_no_key = DisDirectRecursionToDirect(listkey, listvalueNoor)

tuplee = remove_direct_left_recursion(listkey, Direct_list_no_key)

dictre = two_list_to_dict(tuplee[0], tuplee[1])

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
