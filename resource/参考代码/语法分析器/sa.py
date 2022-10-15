###########################################################
#
# 本语法分析器以LL（1）完成
#
###########################################################
import copy

num_grammar_dic = {}  # 语法序号表
grammar_dic = {}  # 语法表
right_grammar_list = []  # 语法表右端
left_grammar = ""  # 语法表左端，即非终结符
s = ""  # 开始符号
#######################读入构建语法表#########################
# 语法表以python的字典存储，键为非终结符，
# 值为该非终结符可以推出的字符串组成的字符串列表
############################################################
f = open("grammar.txt")
line = f.readline()
# 语法序号
ngd_i = 1
s_i = 0
while line:
    # 排除空行
    if line.isspace():
        line = f.readline()
    else:
        # 清除回车
        real_line = line.replace("\n", "")
        # 将含空格单个符号空格替换为下划线，发便使用split分割
        real_line = real_line.replace("GROUP BY", "GROUP_BY")
        real_line = real_line.replace("ORDER BY", "ORDER_BY")
        # 将语法按序号存入语法序号表
        num_grammar_dic[ngd_i] = real_line
        # 拆分语法为左右两部
        split_line = real_line.partition(" -> ")
        # 左端第一次出现，则直接存入语法字典
        if split_line[0] != left_grammar:
            # print(right_grammar_list)
            left_grammar = split_line[0]
            # 将第一个非终结符标记为开始符号S
            if s_i == 0:
                s = left_grammar
                s_i += 1
            right_grammar_list = [split_line[2]]
            grammar_dic[left_grammar] = right_grammar_list
        # 非第一次出现，右端表加入新值
        else:
            right_grammar_list.append(split_line[2])
            grammar_dic[left_grammar] = right_grammar_list
        # print(i, "   ", num_grammar_dic[i])
        ngd_i += 1
        line = f.readline()
f.close
# for i in grammar_dic:
#     print(i, '=', grammar_dic[i])
# for i in num_grammar_dic:
#     print(i, '\t', num_grammar_dic[i])

###########################左FIRST############################
# “构造FIRST集合的算法I”
############################################################
# 非终结符集合
vn = []
# FIRST集字典
first_union = {}
# 用来对比FIRST集是否发生变化
tmp_first_union = {'1': 1}
# 左部FIRST集构造
# 语法字典的键值列表，即非终结符集合
left_first = grammar_dic.keys()
vn = left_first
# 初始化：将所有非终结符加入FIRST集
for vn_i in vn:
    first_union[vn_i] = []
# print(left_first)
# 当FIRST发生变化则循环继续执行
while first_union != tmp_first_union:
    # print("标记")
    # 深拷贝，以免随其改变
    tmp_first_union = copy.deepcopy(first_union)
    # 遍历所有表达式
    for vn_i in vn:
        for rs in grammar_dic[vn_i]:
            # 分割表达式右端字符串，提取字符
            split_rs = rs.split()
            # 终结符的FIRST集只含其本身
            for sr in split_rs:
                if sr not in vn:
                    first_union[sr] = [sr]
            rs_i = 0
            tmp_rs_i = -1
            while rs_i != tmp_rs_i:
                vni_first = []
                tmp_rs_i = rs_i
                # X -> a（或者空集）则把a加入FIRST（X）
                if split_rs[rs_i] not in vn:
                    vni_first.append(split_rs[rs_i])
                    for vf_i in vni_first:
                        first_union[vn_i].append(vf_i)
                    first_union[split_rs[rs_i]] = [split_rs[rs_i]]
                    # 将列表转换为集合再转回列表以消除冗余
                    # 对列表排序，列表值相同顺序不同也不相等
                    for v_j in first_union.keys():
                        first_union[v_j] = list(set(first_union[v_j]))
                        first_union[v_j].sort()
                # 右端不为空集或终结符
                else:
                    # 右端符号串可推出空集则把其各个符号除空集外的FIRST集加入FIRST（X）
                    if split_rs[rs_i] in vn:
                        vni_first = first_union[split_rs[rs_i]]
                        for sr_i in vni_first:
                            if sr_i != '$':
                                first_union[vn_i].append(sr_i)
                    # 右端所有长度的符号串都可以推出空集，则把空集加入（X）
                    if ('$' in grammar_dic[split_rs[rs_i]]) and (
                            rs_i < len(split_rs) - 1):
                        rs_i += 1
                        if (rs_i == len(split_rs) - 1):
                            first_union[vn_i].append('$')
                    # 同上
                    for v_j in first_union.keys():
                        first_union[v_j] = list(set(first_union[v_j]))
                        first_union[v_j].sort()
    # 同上
    for v_j in first_union.keys():
        first_union[v_j] = list(set(first_union[v_j]))
        first_union[v_j].sort()
# print("FIRST:")
# for i in first_union:
#     if (first_union[i] != []) and (i in vn):
#         print('\t', i, '=', first_union[i], ',')
###########################右FIRST############################
# “构造FIRST集合的算法II”
############################################################
# 构建右端字典
rs = {}
# rs键值为表达式右端，值为其分割：X1X2···Xn
for vn_i in grammar_dic:
    for rs_i in grammar_dic[vn_i]:
        if rs_i != '$':
            rs[rs_i] = rs_i.split()
# for rs_i in rs:
#     print(rs_i, ": ", rs[rs_i])
# 右部FIRST集
rs_first_union = {}
for rs_i in rs:
    # 初始化FIRAT（α）=FIRAT（X1）\{空集}
    rs_first_union[rs_i] = copy.deepcopy(first_union[rs[rs_i][0]])
    if '$' in rs_first_union[rs_i]:
        rs_first_union[rs_i].remove('$')
    # FIRST（Xj）含有空集个数
    toemp_i = 0
    for rrs_i in rs[rs_i]:
        if first_union.get(rrs_i):
            if '$' in first_union[rrs_i]:
                toemp_i += 1
    # 均含空集，则在FIRST（α）中加入空集
    if toemp_i == len(rs[rs_i]):
        rs_first_union[rs_i].append('$')
# for i in rs_first_union:
#     if rs_first_union[i] != []:
#         print('\t', i, '=', rs_first_union[i], ',')
# 合并两个FIRST集
first_union.update(rs_first_union)
for v_j in first_union.keys():
    first_union[v_j] = list(set(first_union[v_j]))
    first_union[v_j].sort()
print("****************************FIRST 集*******************************")
print("FIRST:")
for i in first_union:
    print('\t', i, '=', first_union[i], ',')


########################FOLLOW################################
# “构造结合FOLLOW的算法
##############################################################
# 用于求B后β的FIRST集
def fu_func(str):
    spl_str = str.split()
    fu = copy.deepcopy(first_union[spl_str[0]])
    if '$' in fu:
        fu.remove('$')
    toemp = 0
    for sps in spl_str:
        if first_union.get(sps):
            if '$' in first_union[sps]:
                toemp += 1
    if toemp == len(spl_str):
        fu.append('$')
    fu = list(set(fu))
    fu.sort()
    return fu


# test_i=fu_func('functionCall')
# print(test_i)
# for kk in grammar_dic:
#     print(grammar_dic[kk])

follow_union = {}
for vn_i in vn:
    follow_union[vn_i] = []
# 对于开始符号S，置#于FOLLOW（S）中
follow_union[s] = ['#']
tmp_follow_union = {'1': 1}
# 循环直至FOLLOW不再增大
while tmp_follow_union != follow_union:
    tmp_follow_union = copy.deepcopy(follow_union)
    for b in vn:
        # print("FOLLOW:")
        # for i in follow_union:
        #     print('\t', i, '=', follow_union[i], ',')
        for vnn_i in grammar_dic:
            for rs_i in grammar_dic[vnn_i]:
                abc = ['', '', '']
                # 标记B在αBβ中的位置，分割出α、B，β
                if b in rs_i.split():
                    rs_index = 0
                    b_index = -1
                    # B所在位置不同，分割时要考虑如何删除空格
                    for b_i in rs_i.split():
                        if b_i == b:
                            b_index = rs_index
                        rs_index += 1
                    if b_index == 0:
                        if (rs_i.split(b, 1))[1] != '':
                            rs_s = rs_i.split(b + ' ', 1)
                            abc[2] = rs_s[1]
                    elif b_index == len(rs_i.split()) - 1:
                        abc[0] = (list(rs_i.partition(' ' + b)))[0]
                    else:
                        abc[0] = (rs_i.split(' ' + b + ' '))[0]
                        abc[2] = (rs_i.split(' ' + b + ' '))[1]
                    abc[1] = b
                # 找到含B的表达式
                if abc[1] != '':
                    fuc = []
                    # β存在；计算FIRST（β）
                    if (abc[2] != ''):
                        if abc[2] not in first_union:
                            fuc = fu_func(abc[2])
                        else:
                            fuc = first_union[abc[2]]
                        # print(fuc)
                    # β存在；FOLLOW（B）+=FIRST（β）-['$']
                    if abc[2] != '':
                        for c in fuc:
                            if c != '$':
                                follow_union[b].append(c)
                    # β为空；或β存在，且$∈FIRST（β）；FOLLOW（B）+=FOLLOW（A）
                    if abc[2] == '' or '$' in fuc:
                        if vnn_i != b:
                            for a in follow_union[vnn_i]:
                                follow_union[b].append(a)
    # 去冗余、排序
    for fu in follow_union.keys():
        follow_union[fu] = list(set(follow_union[fu]))
        follow_union[fu].sort()
print("****************************FOLLOW 集*******************************")
print("FOLLOW:")
for i in follow_union:
    print('\t', i, '=', follow_union[i], ',')
# print("TMP_FOLLOW:")
# for i in tmp_follow_union:
#     print('\t', i, '=', tmp_follow_union[i], ',')

#########################预测分析表###########################
# 依据"分析表的构造算法"
#############################################################
M = {}
vt = []
# 语法为键，序号为值的字典，方便输出序号
grammar_num_dic = {}
for i in num_grammar_dic:
    grammar_num_dic[num_grammar_dic[i]] = i
# for i in grammar_num_dic:
#     print(i, '\t', grammar_num_dic[i])

# 求终结符集合vt
for vn_i in vn:
    for rs in grammar_dic[vn_i]:
        split_rs = rs.split()
        for sr in split_rs:
            if sr not in vn and sr != '$':
                vt.append(sr)
vt = list(set(vt))
vt.sort()
# print(vt)

# 初始化分析表M
# M为键值为非终结符的字典，
# 其值嵌套另一个字典，该字典的键为所有终结符，值为对应表达式
for vn_i in vn:
    for vt_i in vt:
        M[vn_i] = {}
# 初始化所有格为“ERROR”
for vn_i in vn:
    for vt_i in vt:
        M[vn_i][vt_i] = 'ERROR'

# 给表赋值
for vn_i in grammar_dic:
    for gra in grammar_dic[vn_i]:
        for vt_i in vt:
            gra_first = fu_func(gra)
            gra_sent = vn_i + ' -> ' + gra
            # 语法不存在，非正常情况
            if (gra_sent not in grammar_num_dic):
                print("糟糕")
            # 语法存在
            if vt_i in gra_first:
                M[vn_i][vt_i] = gra_sent
            # 对应算法第（3）步
            if '$' in gra_first:
                for b in follow_union[vn_i]:
                    if b in vt:
                        M[vn_i][b] = vn_i + ' -> $'
# print(
#     "******************************预测分析表*********************************"
# )
# for vn_i in M:
#     print(vn_i, '\t', M[vn_i])

###########################预测分析##########################
input_string = []
f = open("token.tsv")
line = f.readline()
while line:
    # 排除空行
    if line.isspace():
        line = f.readline()
    else:
        # 清除回车
        real_line = line.replace("\n", "")
        real_line = real_line.replace("GROUP BY", "GROUP_BY")
        real_line = real_line.replace("ORDER BY", "ORDER_BY")
        token = real_line.split("\t")
        token[1] = token[1].lstrip('<')
        token[1] = token[1].rstrip('>')
        token.append((token[1].split(','))[1])
        token[1] = token[1].split(',')[0]
        input_string.append(token)
        line = f.readline()
f.close
input_string.append(['#', '#', '#'])
# print(input_string)

print(
    "****************************REDUCTION LIST*******************************"
)
analysis_stack = ['#', s]
index = 1
input_index = 0
gnum = -1
stack_top = s
# 输入串首端为变量则取变量类型，否则直接取值
if input_string[input_index][1] in ['IDN', 'INT', 'FLOAT', 'STRING']:
    input_char = input_string[input_index][1]
else:
    input_char = input_string[input_index][0]
R = "reduction"
MO = "move"
F = "accept"
act = ""
while stack_top != 'ERROR':
    # print(input_char, stack_top)
    # print(analysis_stack)
    gnum = '/'
    # pp = input("next")
    if (stack_top in vt) or (stack_top == '#'):
        # 完成
        if stack_top == input_char and input_char == '#':
            act = F
            analysis_stack.pop()
            print(index, '\t', gnum, '\t', '#', '\t', act)
            break
            #

        # 匹配前进
        elif stack_top == input_char and input_char != '#':
            # 弹出X，ip+1
            act = MO
            analysis_stack.pop()
            input_index += 1
            #
        else:
            print("糟糕")
    # 归约
    else:
        gramy = 'ERROR'
        # 若输入字符已经为空，且分析栈不为空，
        # 则查找分析栈栈顶是否能推出空集
        if input_char == '#':
            fr_st = fu_func(stack_top)
            if '$' in fr_st:
                analysis_stack.pop()
                gnum = grammar_num_dic[stack_top + ' -> $']
                act = R
        # 负责，正常归约
        elif stack_top in vn:
            mmm = M[stack_top]
            gramy = mmm[input_char]
        # 归约成功
        if gramy != 'ERROR':
            # 弹出X，pushYn，根据Yn的长度操作
            act = R
            gnum = grammar_num_dic[gramy]
            y = (gramy.split(' -> '))[1]
            if len(y.split()) > 1:
                yn = y.split()
                yn.reverse()
                analysis_stack.pop()
                for yn_i in yn:
                    if yn_i != '$':
                        analysis_stack.append(yn_i)
                    else:
                        analysis_stack.pop()
            else:
                analysis_stack.pop()
                if y != '$':
                    analysis_stack.append(y)
            #
    # if gnum == '/':
    if input_char == '#':
        print(index, '\t', gnum, '\t', stack_top + '#', '\t', act)
    else:
        print(index, '\t', gnum, '\t', stack_top + '#' + input_char, '\t', act)
    # else:
    #     print(index, '\t', gnum, '\t', stack_top + '#' + input_char, '\t', act,
    #           '\t', num_grammar_dic[gnum])
    # 更新变量
    index += 1
    # 分析栈长度大于1
    if len(analysis_stack) >= 1:
        stack_top = analysis_stack[-1]
    # 非正常情况
    else:
        stack_top = 'ERROR'
    # 输入串首端为变量则取变量类型，负责直接取值
    if input_string[input_index][1] in ['IDN', 'INT', 'FLOAT', 'STRING']:
        input_char = input_string[input_index][1]
    else:
        input_char = input_string[input_index][0]
