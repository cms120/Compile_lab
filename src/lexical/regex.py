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
        for ch in re:

            if ch == '(':
                stack.append(ch)
            elif ch == ')':
                while stack[-1] != '(':
                    postfix.append((stack.pop()))
                # Remove '(' from stack
                stack.pop()
            elif ch in Regex.keyword:  # ch is keyword
                while stack and Regex.keyword[ch] <= Regex.keyword.get(stack[-1], 0):
                    postfix.append((stack.pop()))
                stack.append(ch)
            elif ch == '\\':  # TODO 转义字符
                pass

            else:
                postfix.append(ch)

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
                                                       '(' + ascii_lowercase + '|' + ascii_uppercase + '|' + digits + '|_)*'
_FP = '(' + _INT + '|0).' \
                   '\\.' \
                   '.(' + digits + ')*'

re_c_minus = _INT + '|' + \
             _IDN + '|' + \
             _FP + '|' \
                   '"(ascii)*"|' \
                   '( )*|' \
                   '+|' \
                   '-|' \
                   '\\*|' \
                   '/|' \
                   '%|' \
                   '=|' \
                   '>|' \
                   '<|' \
                   '==|' \
                   '<=|' \
                   '>=|' \
                   '!=|' \
                   '&&|' \
                   '\\|\\||' \
                   ':|' \
                   '\\(|' \
                   '\\)|' \
                   '{|' \
                   '}|' \
                   ';|' \
                   ','  # Regex :c-- TODO 换行未识别 浮点数等符号冲突未解决


def get_re_postfix_c_minus() -> str:  # 获得c--的后缀表达式
    return Regex.get_re_postfix(re_c_minus)
