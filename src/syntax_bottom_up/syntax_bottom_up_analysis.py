import string

import src.lexical.lexical_analysis as la
from src.lexical.token import Token
from src.syntax.grammar import Grammar, get_grammar_c_minus
from src.syntax.syntax_tree import SyntaxTree, SyntaxTreeNode
from src.util import read_file


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


# 把c_minus_grammar.txt转成dict，存的元素如：'compUnit': ['(', 'decl', '|', 'funcDef', ')', '*', 'EOF']
def GrammartextTodict() -> dict:
    grammar = Grammar()
    content = read_file('src/syntax/c_minus_grammar.txt')
    lines = content.split('\n')
    GrammarDict = {}
    for line in lines:
        i = 0
        while line[i] in string.digits + '. ':  # 跳过序号
            i += 1
        line = line[i:]
        if line.endswith(';'):
            line = line[:-1]
        lineList = line.split(' -> ')
        GrammarDict[lineList[0]] = lineList[1].split(' ')
    return GrammarDict


def twoListTodict(listkey: list, listvalue: list):
    dictt = {}
    for i in range(len(listkey)):
        newlist = []
        for j in range(len(listvalue[i])):
            if not j == len(listvalue[i]) - 1:
                newlist += listvalue[i][j] + ['|']
            else:
                newlist += listvalue[i][j]
        listvalue[i] == listvalue[i]
        dictt[listkey[i]] = newlist
    return dictt


# 以‘|’分割列表
def getnoOrList(
        listhaveOr: list):  # 例:把listhaveOr:[['a','|','S','a'],['b','|','R','b']]转成listvaluenoOr[[['a'],['S','a']],[['b'],['R','b']]]
    listvaluenoOr = []
    for listR in listhaveOr:
        listt = []
        listnoOr = []
        for i in range(len(listR)):
            if listR[i] == '|':
                listnoOr.append(listt)
                listt = []
            if i == len(listR) - 1:
                listt.append(listR[i])
                listnoOr.append(listt)
                listt = []
            if not (listR[i] == '|' or i == len(listR) - 1):
                listt.append(listR[i])
        listvaluenoOr.append(listnoOr)

    return listvaluenoOr
    pass


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
    pass


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

    pass


# 间接左递归转直接左递归,返回修改后的listvaluenoOr，如：[[['a'],['S','a']],[['b'],['R','b']]](R的value转成的列表和Q的value组成的列表) -> [[['a'],['S','a']],[['b'],[['S','a','b'],['a','b']]]
def DisDirectRecursionToDirect(listkey: list, listvaluenoOr: list):
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
    pass


def remove_left_recursion():  # TODO 消除一个文法的左递归
    # grammar_list = ['R -> a | S a','Q -> b | R b','S -> c | Q c']
    # {'R':['a','|','S','a'],Q:['b','|','R','b']}

    # 获得c--文本转化的字典
    dictLeftRight = GrammartextTodict()
    # 把字典的键和值分别转换成列表
    listkey = list(dictLeftRight.keys())
    listvalue = dictLeftRight.values()
    # 值列表去除‘|’，以其分割成多个子列表，便于后续转成直接左递归
    listvaluenoOr = getnoOrList(listvalue)
    # 间接左递归转成直接左递归
    newlistvaluenoOr = DisDirectRecursionToDirect(listvaluenoOr)
    # 消除直接左递归，返回一个字典，tuple[0]是键列表，tuple[1]是值列表
    tuple_of_listofKeyValue = remove_direct_left_recursion(listkey, newlistvaluenoOr)
    # 把结果再转化成字典，格式与GrammartextTodict()统一
    indirect_dict = twoListTodict(tuple_of_listofKeyValue[0], tuple_of_listofKeyValue[1])
    # 化简
    simplified_indirect_dict = simplified(indirect_dict)

    return simplified_indirect_dict
    pass


def remove_recall(g: dict):  # TODO 消除回溯
    llr = []
    for u in g:

        g[u] = ' '.join(g[u])
        g[u] = g[u].split('| ')
        for i in range(len(g[u])):
            g[u][i] = ''.join(g[u][i])
            g[u][i] = g[u][i].split(' ')
        llr.append([u, g[u]])
    for k1 in range(len(llr)):
        for k2 in range(len(llr[k1][1]) - 1):
            llr[k1][1][k2].pop()

    # print(llr)
    num = 0
    g_r = {}
    while num == 0:
        # print(llr)
        nllr1 = []
        for i in range(len(llr)):
            newd1 = {}
            dict1 = {}  # key:产生式后端的首个符号,val:其后面可能的的符号
            for j in range(len(llr[i][1])):  # 同上遍历
                a = llr[i][1][j][0]
                dict1.setdefault(a, [])
                # print (dict1)
                # print(llr[i][1][j])
                # print(llr[i][1][j][1:])
                if llr[i][1][j][1:] != []:  # 某符号后有一个及以上符号，正常分开
                    dict1[llr[i][1][j][0]].append(llr[i][1][j][1:])
                    # print(dict1)
                else:  # 否则添加epsilon符号
                    dict1[llr[i][1][j][0]].append(['$'])

            newd1.setdefault(llr[i][0], [])
            for fu in dict1.keys():
                # print(dict1)
                if len(dict1[fu]) == 1:  # 无回溯
                    if ['$'] not in dict1[fu]:
                        newd1[llr[i][0]].append([fu] + dict1[fu][0])
                    else:
                        newd1[llr[i][0]].append([fu])

                    # print(newd1)
                else:
                    newstr = str(llr[i][0]) + 's'  # 新建产生式左端为原产生式左端加s，即S变为S和Ss
                    newd1[llr[i][0]].append([fu] + [newstr])
                    newd1.setdefault(newstr, dict1[fu])
                    # newd1[newstr].append(dict1[fu])
            for fu1 in newd1.keys():
                nllr1.append([fu1, newd1[fu1]])  # 更新nllr1
        if nllr1 == llr:
            num = 1
        else:
            llr = copy.deepcopy(nllr1)
    for i in range(len(llr)):
        g_r.setdefault(llr[i][0], llr[i][1])
    # print(g_r)
    listA = {}
    for l in g_r:

        listA.setdefault(l, [])

        for listU in g_r[l]:
            if not listA[l] == []:
                listA[l].append('|')
            for unit in listU:
                listA[l].append(unit)
    # print(listA[l])
    return listA

    pass


def analysis_with_back(g: Grammar, tokens: list[Token]) -> SyntaxTree:  # 带有回溯的分析一个token list TODO 不能含有左递归
    # 应该是没用了
    s_node = SyntaxTreeNode(g.s)
    tree = SyntaxTree(s_node)

    token_p = 0  # token指针
    while token_p != len(tokens):
        pass

    return tree


def analysis_without_back(g: Grammar, tokens: list[Token]) -> SyntaxTree:  # TODO
    remove_left_recursion(g)
    remove_recall(g)

    s_node = SyntaxTreeNode(g.s)
    tree = SyntaxTree(s_node)

    return tree
