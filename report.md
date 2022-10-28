# Compile_lab_report

对项目的开发过程进行详细的描述

## lexical

词法分析器算法描述，输出格式说明， 源程序编译步骤；

### 分析过程

#### 1 手写c--的正则表达式

#### 2 将regex转换为re_postfix

#### 3 根据re_postfix构造Rules

1. [参考1](https://blog.csdn.net/m0_52293362/article/details/126368664?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522166575589816782417024237%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=166575589816782417024237&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-7-126368664-null-null.142^v56^control,201^v3^control&utm_term=%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F%E6%9E%84%E9%80%A0nfa&spm=1018.2226.3001.4187)
2. [参考2](https://blog.csdn.net/tch3430493902/article/details/102489344?spm=1001.2101.3001.6650.7&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-7-102489344-blog-102981220.t0_edu_mix&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-7-102489344-blog-102981220.t0_edu_mix&utm_relevant_index=14)

#### 4 根据Rules构造FA

fa的数据结构

```python
def __init__(self, k: set[str],
             letters: set[str],
             f: dict[tuple[str, str], set[str]],  # 转换函数 存储start letter ends
             s: str,
             z: set[str]):
  self.k = k  # 状态集
  self.letters = letters  # 字母表
  self.f = f  # 转换函数集 示例 f(S,0)={V,Q} 那么在list中存入的是 ( (S,0) , [V,Q] )
  self.s = s  # 唯一初态
  self.z = z  # 终态集
```

rules与fa的f（转换函数）极为相似，因此构造较为简单

1. 维护一个栈，将起始rules的start压栈，并且根据rules的start赋值fa的初态
2. 不断从栈中推出state并且据此维护fa的状态集和字符集，根据state的两个transition得到与其联系的state压入栈中

#### 5 将NFA确定化

**输入**:一个 NFA N
**输出**:一个接受(识别)相同语言的 DFA M

利用构造 $\epsilon-$ 闭包的方法将NFA确定化为DFA

##### $\epsilon - $闭包

设 I 是 NFA N 的一个状态子集, $\epsilon - CLOSURE(I)$ 定义如下:

1. 若 $s \in I$, 则 $s \in \epsilon - CLOSURE(I)$
2. 若 $s \in I$, 那么从 $s$ 出发经过任意 $\epsilon$ 则到达的任何状态 $s'$, $s' \in \epsilon - CLOSURE(I)$

##### 算法过程

1. 置 DFA M 中的状态集 k' 和 z' 为 $\empty$ 集
2. 给出 M 的初态 $s' = \epsilon - CLOSURE({S})$, 并把 $s'$ 压入待访问状态栈
3. 对于待访问状态栈: 如果栈不为空, 则推出一个状态 $T={q_1,q_2,...,q_n}$ , 
   1. 将 $T$ 加入到已访问状态 set 中
   2. 如果 $T$ 含有一个 N 的终态 那么 $T$ 是 M 的终态
   3. 对于每个 $a \in letters$
      1. $J =f({q_1,q_2,...,q_n},a)=f(q_1,a)\cup f(q_2,a) \cup ... \cup f(q_n,a)$
      2. $U = \epsilon - CLOSURE(J)$
      3. 如果 $J$ 不在已访问set中 将 $J$ 加入待访问状态栈 
   4. 如果 $U$ 不在
4. 重复步骤4，直到栈为空

##### 示例

###### FA

<div STYLE="page-break-after: always;"></div>

<img src="/Users/shan/py/Compile_lab/report.assets/fa.svg" style="zoom: 16%">

<div STYLE="page-break-after: always;"></div>

###### DFA

![dfa](/Users/shan/py/Compile_lab/report.assets/dfa.svg)

#### 6 将DFA最小化

![dfa](/Users/shan/py/Compile_lab/report.assets/dfa.svg)



![dfa_min](/Users/shan/py/Compile_lab/report.assets/dfa_min-6928255.svg)

#### 7 根据DFA分析程序

1. 根据传入字符串构造token TODO
2. 正则表达式关键字的翻译 好像不用
3. 后缀表达式修改

### 输出格式说明

### 附录1 graph

调用了graphviz库，将dfa方便的可视化，便于调试程序以及看到结果

```python
def graph_dfa_print(dfa: DFA):  # 画NFA的图像

  g = Digraph('G', filename='DFA' + str(Graph.dfa_name) + '.gv', format='png')
  for f in dfa.f.items():
    g.edge(f[0][0], f[1], f[0][1])

    g.node(dfa.s, color='res')  # 开始节点红色
    for z in dfa.z:
      g.node(z, shape='doublecircle')  # 结束节点双层

      Graph.dfa_name += 1

      g.view()
```

导出为svg图片

```shell
 dot DFA.gv -T svg -o dfa.svg
```

## syntax

（2）语法分析器的算法描述，创建的分析表（预测分析表、LR 分析表等），输出格式说明，源程序编译步骤。

1. 手动构造c--文法
    - ![image-20221020200324493](README.assets/image-20221020200324493.png)
2. 根据token串将其理解为各类语法单位：短语、子句、程序段、程序。输出语法树

### syntax_bottom_up LL

#### LL(1) 每一步只向前查看一个符号

1. 消除左递归
    1. 消除一个产生式直接左递归
    2. 消除一个文法的左递归
2. 消除回溯、提取左因子
    - 反复提取所有非终结符左因子，使得一个文法的所有非终结符的所有候选首符集两两不相交


LL(1)分析条件：

1. 一个文法不含左递归
2. 所有非终结符的所有候选首符集两两不相交
3. 对于每个非终结符A，若某个候选首符集包含$\epsilon$，那么他的First与Follow集交集为空

前两点可以通过算法解决，最后一点c--不一定符合，如果c--不符合，还需要回溯机制

### syntax_top_down LR

#### 算符优先分析法

#### LR分析法

## Semantic

（3）存储，遍历语法树的过程算法伪代码，以及调用中端的过程的算法设计思想。 

1. 静态语义检查
2. 中间代码的翻译
