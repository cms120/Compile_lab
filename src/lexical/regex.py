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


re_c_minus = '(1-9).(0-9)* | (a-z|A-Z|_).(a-z|A-Z|_|0-9)* | (0-9)*.(.).(0-9)* | "(letters)*" | | + | - | * | / | % | = | > | < | == | <= | >= | != | && | || |：|（ | ）| {  | } | ；| ,'  # Regex :c-- TODO 换行未识别 浮点数等符号冲突未解决


def get_re_postfix_c_minus() -> str:  # 获得c--的后缀表达式
    return Regex.get_re_postfix(re_c_minus)
