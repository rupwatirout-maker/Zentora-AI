import ast
import math
import operator


class CalculatorTool:
    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    _functions = {
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "log10": math.log10,
        "abs": abs,
        "round": round,
    }

    @classmethod
    def calculate(cls, expression: str):
        tree = ast.parse(expression, mode="eval")
        return cls._evaluate(tree.body)

    @classmethod
    def _evaluate(cls, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)) and not isinstance(
                node.value, bool
            ):
                return node.value

            raise ValueError("Unsupported value.")

        if isinstance(node, ast.BinOp):
            operation = cls._operators.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operator.")

            left = cls._evaluate(node.left)
            right = cls._evaluate(node.right)

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):
            operation = cls._operators.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported unary operator.")

            return operation(cls._evaluate(node.operand))

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Unsupported function.")

            function = cls._functions.get(node.func.id)

            if function is None:
                raise ValueError("Unsupported function.")

            arguments = [cls._evaluate(argument) for argument in node.args]

            return function(*arguments)

        raise ValueError("Unsupported expression.")

    @classmethod
    def format_result(cls, result):
        if isinstance(result, float) and result.is_integer():
            return str(int(result))

        return str(result)
