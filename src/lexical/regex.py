from collections import deque


class Regex:
    keyword = {'*': 50,  # 闭包
               '.': 40,  # 连接
               '|': 30,  # 或
               '(': 20,
               ')': 10
               }  # 正则表达式的关键字

    @staticmethod
    def get_re_postfix(re: str) -> str:  # 得到后缀表达式 a.b -> ab.
        postfix = deque()
        stack = deque()

        # Loop through the string one character at a time
        it = iter(range(len(re)))
        for i in it:

            if re[i] == '(':
                stack.append(re[i])
            elif re[i] == ')':
                while stack[-1] != '(':
                    postfix.append((stack.pop()))
                # Remove '(' from stack
                stack.pop()
            elif re[i] in Regex.keyword:  # re[i] is keyword
                while stack and Regex.keyword[re[i]] <= Regex.keyword.get(stack[-1], 0):
                    postfix.append((stack.pop()))
                stack.append(re[i])
            elif re[i] == '\\':  # TODO 转义字符
                postfix.append(re[i])
                # postfix.append(re[i])
                postfix.append(re[i + 1])
                next(it)
            else:
                postfix.append(re[i])

        while stack:
            postfix += (stack.pop())

        res = ''
        while postfix:
            res += postfix.popleft()
        return res


ascii_lowercase = 'a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z'
ascii_uppercase = ascii_lowercase.upper()
digits_without_zero = '1|2|3|4|5|6|7|8|9'
digits = '0|' + digits_without_zero

_INT = '(' + digits_without_zero + ').(' + digits + ')*'  # 常数
_IDN = '(' + ascii_lowercase + '|' + ascii_uppercase + '|_)' \
                                                       '.' \
                                                       '(' + ascii_lowercase + '|' + ascii_uppercase + '|' + \
       digits + '|_)*'
_FP = '(' + _INT + '|0).' \
                   '\\.' \
                   '.(' + digits + ')*'

# STR只支持了c--中字符以及部分必要字符
_STR = ascii_lowercase + '|' + ascii_uppercase + '|' + digits + '+|-|\\*|/|%|=|>|<|!|&|:|;|{|}|\\(|\\)|,| |\n|\t'

re_c_minus = _INT + '|' + \
             _IDN + '|' + \
             '+|' + \
             '-|' + \
             '\\*|' + \
             '/|' + \
             '%|' + \
             '=|' + \
             '>|' + \
             '<|' + \
             '=.=|' + \
             '<.=|' + \
             '>.=|' + \
             '!.=|' + \
             '&.&|' + \
             '\\|.\\||' + \
             ':|' + \
             '\\(|' + \
             '\\)|' + \
             '{|' + \
             '}|' + \
             ';|' + \
             ','  # Regex :c-- TODO 换行未识别 浮点数等符号冲突未解决


def get_re_postfix_c_minus() -> str:  # 获得c--的后缀表达式
    return Regex.get_re_postfix(re_c_minus)
