# Compile_lab

## lexical

分析过程

1. 手写c--的正则表达式 TODO
2. 将正则表达式转换成后缀表达式 done
3. 根据后缀表达式构造Rules done
4. 根据Rules构造NFA done
    1. [参考1](https://blog.csdn.net/m0_52293362/article/details/126368664?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522166575589816782417024237%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=166575589816782417024237&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-7-126368664-null-null.142^v56^control,201^v3^control&utm_term=%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F%E6%9E%84%E9%80%A0nfa&spm=1018.2226.3001.4187)
    2. [参考2](https://blog.csdn.net/tch3430493902/article/details/102489344?spm=1001.2101.3001.6650.7&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-7-102489344-blog-102981220.t0_edu_mix&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-7-102489344-blog-102981220.t0_edu_mix&utm_relevant_index=14)
5. NFA确定化 done
6. DFA最小化 TODO
7. 根据DFA分析程序 TODO
   1. 根据传入字符串构造token TODO 
   2. 正则表达式关键字的翻译 TODO
   3. 后缀表达式修改 TODO

## syntax
1. 手动构造c--文法
   - ![image-20221020200324493](README.assets/image-20221020200324493.png)
2. 根据token串将其理解为各类语法单位：短语、子句、程序段、程序。输出语法树

### syntax_bottom_up LL
#### LL(1) 每一步只向前查看一个符号
1. 消除左递归
   1. 消除直接左递归
   2. 消除左递归
2. 消除回溯、提取左因子
### syntax_top_down LR

#### 算符优先分析法

#### LR分析法


## Semantic
1. 静态语义检查
2. 中间代码的翻译