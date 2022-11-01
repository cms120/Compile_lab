import src.lexical.lexical_analysis as la
from lexical.token import Token
from src.syntax.grammar import Grammar, get_g_c_minus_auto,Production
from src.syntax.syntax_tree import SyntaxTree, SyntaxTreeNode
from src.syntax.syntax_unit import SyntaxUnit


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
    return analysis_without_back(get_g_c_minus_auto(),
                                 la.analysis())

#把c_minus_grammar.txt转成dict，存的元素如：'compUnit': ['(', 'decl', '|', 'funcDef', ')', '*', 'EOF']
def GrammartextTodict() ->dict:
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

"""
TurnGrammartoList
目的是构建一个四维队列来存文法结构(右部以'|'分割)
如： 传进文法'R -> a | S a','Q -> b | R b','S -> c | Q c'
转成 : [[unit_R,[[unit_a],[unit_S,unit_a]]] , [unit_Q,[[Unit_b],[unit_R,unit_b]]] , [unit_S,[[unit_c],[unit_Q,unit_c]]]]
便于后续转换操作

"""
def TurnGrammartoList(g:Grammar):
    listLeftRight = []  #四维队列 元素是三维队列[UnitS,[[Unita],[Unitb,Unitc]]]
    
    for production in g.productions:
        threeList= []
        right_doublelist = []#二维队列 如[[Unita],[Unitb,Unitc]]
        sinlist = [] #一维队列 如[Unita]或[Unitb,Unitc] ，以‘|’区分
        for unit in production.right:
            if  unit.name == 'regex_line' :
                right_doublelist.append(sinlist)
                sinlist = []
            if  unit==production.right[-1]:
                sinlist.append(unit)
                right_doublelist.append(sinlist)
                sinlist = []
            else:
                sinlist.append(unit)
        
        threeList.append([production.left,right_doublelist])
        listLeftRight.append(threeList)
        threeList= []
        # print(listLeftRight)
    return listLeftRight
    pass

#把listLeftRight转成Grammar 
def TurnListToGrammar(listLeftRight:list):
    g = Grammar()
    for l in listLeftRight:
        listAddOr = []
        for listU in l[1]:
            if not listAddOr == []:
                listAddOr.append(SyntaxUnit('|'))  
            for unit in listU:              
                listAddOr.append(unit)
        p = Production(l[0],tuple(listAddOr)) 
        g.productions.append(p)
    
    return g 
    pass


def remove_left_recursion(g: Grammar):  # TODO 消除一个文法的左递归
    #建立dictLeftRight：文法的左边为key，右边以|分裂存在tuple
    listLeftRight = TurnGrammartoList(g)
    g_result = Grammar()
    
        
    for i in range(len(listLeftRight)):# 以listLeftRight=[[unit_R,[[unit_a],[unit_S,unit_a]]] , [unit_Q,[[Unit_b],[unit_R,unit_b]]] , [unit_S,[[unit_c],[unit_Q,unit_c]]]]为例
        for j in range(i):
            for k in range(len(listLeftRight[i][1])):#[[unit_a],[unit_S,unit_a]]
                if listLeftRight[i][1][k][0] ==  listLeftRight[j][0]: #例如：listLeftRight[1][1][1][0]=unit_R = listLeftRight[0][0]
                    lastlist = listLeftRight[i][1][k][1:] # [unit_R,unit_b]转成[unit_b]
                    del listLeftRight[i][1][k] 
                    for frontlist in listLeftRight[j][1]: 
                        newlist =  frontlist + lastlist   # [unit_a]+[unit_b]或[unit_S,unit_a]+[unit_b]   
                        listLeftRight[i][1].append(newlist) #以[unit_Q,[[Unit_b],[unit_R,unit_b]]]为例，变成了[unit_Q,[[Unit_b],[unit_a,unit_b],[unit_S,unit_a,unit_b]]]
    # #消除直接左递归
    # for liLR in  listLeftRight:
    #     for li in liLR[1]:
    #         if li[0] == liLR[0]:
    #             RemovedDirectList = remove_direct_left_recursion(liLR)
    #             listLeftRight=[RemovedDirectList if i ==liLR else i for i in listLeftRight]

    g_result = TurnListToGrammar(listLeftRight)    
    
    return g_result 
    pass


def remove_recall(g: Grammar):  # TODO 消除回溯
    pass


def analysis_with_back(g: Grammar, tokens: list[Token]) -> SyntaxTree:  # 带有回溯的分析一个token list TODO 不能含有左递归
    # 应该是没用了
    s_node = SyntaxTreeNode(SyntaxUnit.Program)
    tree = SyntaxTree(s_node)

    token_p = 0  # token指针
    while token_p != len(tokens):
        pass

    return tree


def analysis_without_back(g: Grammar, tokens: list[Token]) -> SyntaxTree:  # TODO
    remove_left_recursion(g)
    remove_recall(g)

    s_node = SyntaxTreeNode(SyntaxUnit.Program)
    tree = SyntaxTree(s_node)

    return tree
