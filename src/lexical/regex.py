class Regex:
    __regex_keyword = {'*': 50,  # 闭包
                       '.': 40,  # 连接
                       '|': 30  # 或
                       }  # 正则表达式的关键字

    @staticmethod
    def get_re_postfix(re: str) -> str:  # 得到后缀表达式 a.b -> ab.
        postfix = ""
        stack = ""

        # Loop through the string one character at a time
        for ch in re:
            if ch == '(':
                stack = stack + ch
            elif ch == ')':
                while stack[-1] != '(':
                    postfix, stack = postfix + stack[-1], stack[:-1]
                # Remove '(' from stack
                stack = stack[:-1]
            elif ch in Regex.__regex_keyword:
                while stack and Regex.__regex_keyword.get(ch, 0) <= Regex.__regex_keyword.get(stack[-1], 0):
                    postfix, stack = postfix + stack[-1], stack[:-1]
                stack = stack + ch
            else:
                postfix = postfix + ch

        while stack:
            postfix, stack = postfix + stack[-1], stack[:-1]

        return postfix


re_c_minus = '(a|b)*c'  # Regex :c-- TODO


def get_re_postfix_c_minus() -> str:  # 获得c--的后缀表达式
    return Regex.get_re_postfix(re_c_minus)
