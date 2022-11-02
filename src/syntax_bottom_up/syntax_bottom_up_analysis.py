from typing import List

import src.lexical.lexical_analysis as la
from src.lexical.token import Token
from src.syntax.grammar import Grammar, get_grammar_c_minus
from src.syntax.syntax_tree import SyntaxTree, SyntaxTreeNode


# 根据文法来分析token list


def check_left_recursion(g: Grammar) -> bool:  # 检查一个文法是否有左递归
    pass


def check_first(g: Grammar) -> bool:  # 检查一个文法的first集
    first_dict = g.get_first()
    pass


def check_follow(g: Grammar) -> bool:  # 检查一个文法的follow集
    follow_dict = g.get_follow()
    pass


def check_if_ll_one(g: Grammar) -> bool:  # 检查一个文法是否是ll(1)
    return check_follow(g) and check_first(g) and check_left_recursion(g)


def analysis() -> SyntaxTree:  # c--的语法分析
    return analysis_without_back(get_grammar_c_minus(),
                                 la.analysis())


def two_list_to_dict(listkey: list, listvalue: list):
    dict_t = {}
    for i in range(len(listkey)):
        new_list = []
        for j in range(len(listvalue[i])):
            if not j == len(listvalue[i]) - 1:
                new_list += listvalue[i][j] + ['|']
            else:
                new_list += listvalue[i][j]
        listvalue[i] == listvalue[i]
        dict_t[listkey[i]] = new_list
    return dict_t


#
def get_no_or_list(list_have_or: List[List[str]]) -> List[List[List[str]]]:
    """
    以‘|’分割列表
    compUnit -> ( decl | funcDef ) * EOF

    :param list_have_or:[['a','|','S','a'],['b','|','R','b']]

    :returns: [[['a'],['S','a']],[['b'],['R','b']]]
    """
    # TODO 括号的问题
    list_value_no_or = []
    for listR in list_have_or:
        list_t = []
        list_no_or = []
        for i in range(len(listR)):
            if listR[i] == '|':
                list_no_or.append(list_t)
                list_t = []
            if i == len(listR) - 1:
                list_t.append(listR[i])
                list_no_or.append(list_t)
                list_t = []
            else:
                list_t.append(listR[i])
        list_value_no_or.append(list_no_or)

    return list_value_no_or


# 消除直接左递归, 返回一个元组tuplee，tuplee[0]为修改后的listkey，tuplee[1]为修改后的listvalue
def remove_direct_left_recursion(listkey: list, listvalue: list):
    memory = []
    haveRecursion = 0
    for i in range(len(listvalue)):  # listvalue格式如：[[unit_c],[unit_S,unit_a,unit_b,unit_c]]
        lists = []
        for k in range(len(listvalue[i])):

            if listvalue[i][k][0] == listkey[i]:
                haveRecursion = 1
                memory.append(listvalue[i][k][1:])  # 记录，如[unit_S,unit_a,unit_b,unit_c]转成[Unit_a,unit_b,unit_c]
                lists.append(k)
        if haveRecursion == 1:
            for number in lists:
                del listvalue[i][number]
            # SyntaxTree(unit.name+ss)=unit.value+'`'
            newlist = []
            for j in range(len(listvalue[i])):
                listvalue[i][j].append(listkey[i] + '`')
                newlist = []  # 即['S`',[]]
            for l in memory:
                newlist.append(l + [listkey[i] + '`'])
            newlist.append(['$'])

            listvalue.append(newlist)
            listkey.append(listkey[i] + '`')

    tuplee = (listkey, listvalue)

    return tuplee


def simplified(dic: dict):  # 化简 TODO
    newdict = {'Program': ['compUnit']}
    listkey = list(newdict.keys())
    for key in listkey:
        for value in newdict[key]:
            if not value in listkey and (value.isalpha() or value == key + '`') and not value == 'EOF':
                newdict[value] = dic[value]
                listkey.append(value)
                print('value=', value)
    return newdict


def DisDirectRecursionToDirect(listkey: list, listvaluenoOr: list):
    """
    间接左递归转直接左递归,返回修改后的listvaluenoOr，如：

    [[['a'],['S','a']],[['b'],['R','b']]](R的value转成的列表和Q的value组成的列表)
    -> [[['a'],['S','a']],[['b'],[['S','a','b'],['a','b']]]

    """
    for i in range(len(listkey)):
        for j in range(i):
            for k in range(len(listvaluenoOr[i])):
                if listvaluenoOr[i][k][0] == listkey[j]:
                    lastlist = listvaluenoOr[i][k][1:]
                    del listvaluenoOr[i][k]
                    for headlist in listvaluenoOr[j]:
                        newlist = headlist + lastlist
                        listvaluenoOr[i].append(newlist)

    return listvaluenoOr


def remove_left_recursion(g: Grammar):  # TODO 消除一个文法的左递归
    # grammar_list = ['R -> a | S a','Q -> b | R b','S -> c | Q c']
    # {'R':['a','|','S','a'],Q:['b','|','R','b']}

    # 获得c--文本转化的字典
    dictLeftRight = g.productions
    # 把字典的键和值分别转换成列表
    listkey = list(dictLeftRight.keys())
    listvalue = dictLeftRight.values()
    # 值列表去除‘|’，以其分割成多个子列表，便于后续转成直接左递归
    listvaluenoOr = get_no_or_list(listvalue)
    # 间接左递归转成直接左递归
    newlistvaluenoOr = DisDirectRecursionToDirect(listvaluenoOr)
    # 消除直接左递归，返回一部字典，tuple[0]是键列表，tuple[1]是值列表
    tuple_of_listofKeyValue = remove_direct_left_recursion(listkey, newlistvaluenoOr)
    # 把结果再转化成字典，格式与GrammartextTodict()统一
    indirect_dict = two_list_to_dict(tuple_of_listofKeyValue[0], tuple_of_listofKeyValue[1])
    # 化简
    simplified_indirect_dict = simplified(indirect_dict)

    return simplified_indirect_dict


def remove_recall(g: Grammar):  # TODO 消除回溯
    pass


def analysis_with_back(g: Grammar, tokens: list[Token]) -> SyntaxTree:  # 带有回溯的分析一个token list TODO 不能含有左递归
    # 应该是没用了
    s_node = SyntaxTreeNode('Program')
    tree = SyntaxTree(s_node)

    token_p = 0  # token指针
    while token_p != len(tokens):
        pass

    return tree


def analysis_without_back(g: Grammar, tokens: list[Token]) -> SyntaxTree:  # TODO
    remove_left_recursion(g)
    remove_recall(g)

    s_node = SyntaxTreeNode('Program')
    tree = SyntaxTree(s_node)

    return tree
