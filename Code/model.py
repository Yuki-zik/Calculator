import re
from decimal import Decimal


# (    )   C  ⌫  %  x²  √x ÷ 7   8   9  × 4   5   6  - 1  2  3  +  0  .  =
def calculate(expression):
    # 替换特殊符号
    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")
    expression = expression.replace("\\", "/")
    expression = expression.replace("²", "^2")
    # expression = expression.replace("√", "^0.5")

    # 使用正则表达式分割表达式
    tokens = re.findall(
        r"(?<![0-9])[+-]?[0-9.]+(?:[Ee][+-]?[0-9]+)?|[-+*/%^√()]", expression
    )

    # 优先级处理函数
    def precedence(op):
        if op in "+-":
            return 1
        if op in "*/%":
            return 2
        if op in "^√":
            return 3
        return 0

    # 中缀表达式转换为后缀表达式
    def infix_to_postfix(tokens):  # -> list[Any]:
        output = []  # 存储后缀表达式
        stack = []  # 操作符栈
        print(tokens)

        for token in tokens:
            try:
                Decimal(token)
                isdigit = True
            except:
                isdigit = False
            if isdigit:  # 判断是否为数字
                output.append(token)
            elif token == "(":
                stack.append(token)
            elif token == ")":
                while stack[-1] != "(":
                    output.append(stack.pop())
                stack.pop()  # 弹出 '('
            else:
                while stack and precedence(stack[-1]) >= precedence(token):
                    output.append(stack.pop())
                stack.append(token)
        while stack:
            output.append(stack.pop())
        return output

    # 后缀表达式求值
    def evaluate_postfix(tokens):
        stack = []
        flag_inverse = False

        for token in tokens:
            try:
                Decimal(token)
                isdigit = True
            except:
                isdigit = False
            if isdigit:  # 判断是否为数字
                stack.append(Decimal(token))
            else:
                operand2 = stack.pop()
                if token == "√":
                    stack.append(operand2 ** Decimal("0.5"))
                else:
                    operand1 = stack.pop()
                    if token == "+":
                        stack.append(operand1 + operand2)
                    elif token == "-":
                        stack.append(operand1 - operand2)
                    elif token == "*":
                        stack.append(operand1 * operand2)
                    elif token == "/":
                        stack.append(operand1 / operand2)
                    elif token == "%":
                        stack.append(operand1 % operand2)
                    elif token == "^":
                        stack.append(operand1**operand2)
        while len(stack) > 1:  # 如果省略乘号按乘法看待
            stack.append(stack.pop() * stack.pop())

        return stack[0]

    postfix_tokens = infix_to_postfix(tokens)
    result = evaluate_postfix(postfix_tokens)

    return result


def main():
    expression = input("请输入表达式: ")
    result = calculate(expression)
    print("结果:", result)


if __name__ == "__main__":
    main()
