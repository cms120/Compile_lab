from src.lexical.finite_automation import FA


class DFA(FA):

    @staticmethod
    def init_by_fa(fa: FA):  # 根据FA构造最小DFA
        return dfa_minimize(
            fa_2_dfa(fa))


def fa_2_dfa(fa: FA) -> DFA:  # NFA确定化

#   一. 不具有e−转移的NFA转具有e−转移的NFA
#    （1）引进初态X和终态Y，X, Y ∈S, 从X到S0中任意状态连接一条
# ε箭弧，从F中任意状态连接一条ε箭弧到Y。
      
#    （2）对M的状态转换图进一步实施如下替换，其中状态2是新引入
# 状态。重复该过程，直到每条箭弧上标记ε，或者为∑中的单个字
# 符。 

#   二.将 e−NFA转化为等价的 DFA
#     (1) 首先从S0出发，仅经过任意条箭弧所能到达的状态所组成的集合I作为M’的
#    初态q0. 

#     (2) 分别把从q0（对应于M的状态子集I）出发，经过任意a∈文法有穷字母表的a弧转换Ia 所
#     组成的集合作为M’ 的状态，如此继续，直到不再有新的状态为止。
    
# 参考代码：
# d = defaultdict(list)
#     t = [] #终结符
#     f = open(path)
#     text = []
#     for l in f:
#         text.append(l)
#     #将文本存入defaultdict中
#     for item in text:
#         if item == '\n':
#             continue
#         item = item.split('\n')
#         item = item[0].split(':')
#         separate = item[1].split('|')
#         for i in separate:
#             latter = i.split(' ')
#             d[str(item[0])].append([str(latter[0]),str(latter[1])])
#     print(d)
#     #子集法进行转换
#     #1、算出每个状态的闭包，空在词法中以 $ 表示
#     closure = defaultdict(list)
#     for key in d.keys():
#         for item in d[key]:
#             if item[0] == '$':
#                 closure[str(key)].append(str(item[1]))
#             else:
#                 if item[0] not in t:
#                     t.append(item[0])
#     #2、找状态
#     DFA = defaultdict(list)    #存储每一个状态里对应的东西
#     ADVANCE = defaultdict(list)    #存储状态转换线路
#     stateNum = 0
#     analyseNum = 0
#     DFA[str(stateNum)].append('start')
#     for item in closure['start']:
#         DFA[str(stateNum)].append(item)
#     while True:
#         F = False
#         for item in DFA[str(stateNum)]:
#             if item in closure.keys():
#                 for value in closure[item]:
#                     if value not in DFA[str(stateNum)]:
#                         DFA[str(stateNum)].append(value)
#                         F = True
#         if F == False:
#             break
#     stateNum += 1
#     while analyseNum != stateNum:
#         for key in t:     #对每个终结符进行遍历
#             temp = []
#             for item in DFA[str(analyseNum)]:
#                 for item1 in d[str(item)]:
#                     if item1[0] == key:
#                         temp.append(item1[1])
#             if len(temp) == 0:
#                 continue
#             #找temp的闭包
#             while True:
#                 F = False    #如果有新加入的元素就变True，否则一直为False跳出while循环
#                 for item in temp:
#                     for p in closure[item]:
#                         if p not in temp:
#                             temp.append(p)
#                             F = True
#                 if F == False:
#                     break

#             flag = False  #判断是否已经存在这个状态，False代表不存在，True代表存在
#             num = 0
#             for kk in DFA.keys():
#                 num = kk
#                 if len(DFA[kk]) != len(temp):
#                     continue
#                 else:
#                     cnt = 0
#                     for i1 in temp:
#                         if i1 not in DFA[kk]:
#                             break
#                         cnt += 1
#                     if cnt == len(temp):
#                         flag = True
#                         break
#             if flag == False:
#                 for i in temp:
#                     DFA[str(stateNum)].append(i)
#                 ADVANCE[str(analyseNum)].append([str(key),str(stateNum)])
#                 stateNum += 1
#             else:
#                 ADVANCE[str(analyseNum)].append([str(key), str(num)])
#         analyseNum += 1
#     print(DFA)
#     print(ADVANCE)
#     return ADVANCE
#     pass  # TODO


def dfa_minimize(dfa) -> DFA:  # DFA最小化
    # 1.区分初态和末态，各分为一个集合

    # 2.判断集合是否可“区分”

    # 3.对两个集合根据是否可再分继续划分集合，直到不可再划分为止

    pass  # TODO
