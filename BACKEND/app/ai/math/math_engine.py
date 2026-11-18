import ast
import re

import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)


class MathEngine:

    _transformations = standard_transformations + (
        convert_xor,
        implicit_multiplication_application,
    )

    _allowed_symbols = {
        "x": sp.Symbol("x"),
        "y": sp.Symbol("y"),
        "z": sp.Symbol("z"),
        "a": sp.Symbol("a"),
        "b": sp.Symbol("b"),
        "c": sp.Symbol("c"),
        "n": sp.Symbol("n"),
        "t": sp.Symbol("t"),
        "pi": sp.pi,
        "e": sp.E,
    }

    _functions = {
        "sqrt": sp.sqrt,
        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,
        "cot": sp.cot,
        "sec": sp.sec,
        "csc": sp.csc,
        "asin": sp.asin,
        "acos": sp.acos,
        "atan": sp.atan,
        "log": sp.log,
        "ln": sp.log,
        "exp": sp.exp,
        "abs": sp.Abs,
    }

    @classmethod
    def _normalize_text(cls, text: str) -> str:
        normalized = text.strip().lower()

        replacements = {
            "×": "*",
            "✕": "*",
            "✖": "*",
            "÷": "/",
            "−": "-",
            "–": "-",
            "—": "-",
            "π": "pi",
            "²": "**2",
            "³": "**3",
        }

        for old, new in replacements.items():
            normalized = normalized.replace(old, new)

        normalized = re.sub(r"\bmultiplied by\b", "*", normalized)
        normalized = re.sub(r"\btimes\b", "*", normalized)
        normalized = re.sub(r"\bdivided by\b", "/", normalized)
        normalized = re.sub(r"\bplus\b", "+", normalized)
        normalized = re.sub(r"\bminus\b", "-", normalized)

        return normalized

    @classmethod
    def _clean_expression(cls, text: str) -> str:
        text = cls._normalize_text(text)

        prefixes = (
            "calculate ",
            "calc ",
            "compute ",
            "evaluate ",
            "simplify ",
            "solve ",
            "find ",
        )

        for prefix in prefixes:
            if text.startswith(prefix):
                text = text[len(prefix):].strip()
                break

        text = re.sub(r"^(what is|what's)\s+", "", text)

        return text.rstrip("?").strip()

    @classmethod
    def _parse(cls, expression: str):
        local_dict = {
            **cls._allowed_symbols,
            **cls._functions,
        }

        return parse_expr(
            expression,
            local_dict=local_dict,
            transformations=cls._transformations,
            evaluate=True,
        )

    @classmethod
    def _parse_matrix(cls, text: str):
        normalized = cls._normalize_text(text)

        matrix_match = re.search(
            r"\[\s*\[.*\]\s*\]",
            normalized,
        )

        if not matrix_match:
            return None

        matrix_text = matrix_match.group(0)

        try:
            rows = ast.literal_eval(matrix_text)
        except (ValueError, SyntaxError):
            return None

        if not isinstance(rows, list):
            return None

        if not rows or not all(isinstance(row, list) for row in rows):
            return None

        if len({len(row) for row in rows}) != 1:
            return None

        if not all(
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            for row in rows
            for value in row
        ):
            return None

        return sp.Matrix(rows)

    @classmethod
    def _looks_like_math(cls, text: str) -> bool:
        normalized = cls._normalize_text(text)

        indicators = (
            "+",
            "-",
            "*",
            "/",
            "=",
            "^",
            "sqrt",
            "sin",
            "cos",
            "tan",
            "cot",
            "sec",
            "csc",
            "log",
            "ln",
            "matrix",
            "determinant",
            "det",
            "inverse",
            "differentiate",
            "derivative",
            "integrate",
            "integral",
            "simplify",
            "solve",
        )

        if any(indicator in normalized for indicator in indicators):
            return True

        if re.search(r"\d", normalized):
            words = (
                "calculate",
                "compute",
                "solve",
                "evaluate",
                "find",
                "what is",
                "what's",
                "into",
                "times",
                "divided",
                "plus",
                "minus",
            )

            return any(word in normalized for word in words)

        return False

    @classmethod
    def _parse_natural_arithmetic(cls, text: str):
        normalized = cls._normalize_text(text)

        match = re.fullmatch(
            r"(\d+(?:\.\d+)?)\s+into\s+(\d+(?:\.\d+)?)",
            normalized,
        )

        if match:
            left, right = match.groups()
            return cls._parse(f"{left} * {right}")

        return None

    @classmethod
    def calculate(cls, expression: str):
        expression = cls._clean_expression(expression)

        natural_result = cls._parse_natural_arithmetic(expression)

        if natural_result is not None:
            return sp.simplify(natural_result)

        return sp.simplify(cls._parse(expression))

    @classmethod
    def solve_equation(cls, equation: str):
        equation = cls._clean_expression(equation)
        equation = equation.replace("==", "=")

        if "=" not in equation:
            raise ValueError("Equation must contain '='.")

        left, right = equation.split("=", 1)

        lhs = cls._parse(left.strip())
        rhs = cls._parse(right.strip())

        return sp.solve(sp.Eq(lhs, rhs))

    @classmethod
    def simplify(cls, expression: str):
        return sp.simplify(
            cls._parse(
                cls._clean_expression(expression)
            )
        )

    @classmethod
    def differentiate(cls, expression: str, variable="x"):
        variable_symbol = cls._allowed_symbols.get(variable)

        if variable_symbol is None:
            raise ValueError("Unsupported differentiation variable.")

        parsed = cls._parse(
            cls._clean_expression(expression)
        )

        return sp.diff(parsed, variable_symbol)

    @classmethod
    def integrate(cls, expression: str, variable="x"):
        variable_symbol = cls._allowed_symbols.get(variable)

        if variable_symbol is None:
            raise ValueError("Unsupported integration variable.")

        parsed = cls._parse(
            cls._clean_expression(expression)
        )

        return sp.integrate(parsed, variable_symbol)

    @classmethod
    def matrix_determinant(cls, text: str):
        matrix = cls._parse_matrix(text)

        if matrix is None:
            raise ValueError("A valid matrix is required.")

        return matrix.det()

    @classmethod
    def matrix_inverse(cls, text: str):
        matrix = cls._parse_matrix(text)

        if matrix is None:
            raise ValueError("A valid matrix is required.")

        return matrix.inv()

    @classmethod
    def matrix_transpose(cls, text: str):
        matrix = cls._parse_matrix(text)

        if matrix is None:
            raise ValueError("A valid matrix is required.")

        return matrix.T

    @classmethod
    def format_result(cls, result):
        if isinstance(result, list):
            if not result:
                return "No solution found."

            return ", ".join(
                cls.format_result(item)
                for item in result
            )

        if isinstance(result, tuple):
            return (
                "("
                + ", ".join(
                    cls.format_result(item)
                    for item in result
                )
                + ")"
            )

        if isinstance(result, sp.MatrixBase):
            return str(result)

        return str(sp.simplify(result))

    @classmethod
    def answer(cls, message: str):
        text = message.strip()

        if not text or not cls._looks_like_math(text):
            return None

        normalized = cls._normalize_text(text)

        try:
            matrix = cls._parse_matrix(normalized)

            if matrix is not None:
                if "determinant" in normalized or re.search(
                    r"\bdet\b",
                    normalized,
                ):
                    result = matrix.det()

                    return (
                        f"The determinant is "
                        f"{cls.format_result(result)}."
                    )

                if "inverse" in normalized:
                    result = matrix.inv()

                    return (
                        "The inverse is:\n"
                        f"{cls.format_result(result)}"
                    )

                if "transpose" in normalized:
                    result = matrix.T

                    return (
                        "The transpose is:\n"
                        f"{cls.format_result(result)}"
                    )

                if normalized.strip().startswith("["):
                    return (
                        "The matrix is:\n"
                        f"{cls.format_result(matrix)}"
                    )

            if normalized.startswith(
                ("differentiate ", "derivative of ")
            ):
                expression = re.sub(
                    r"^(differentiate|derivative of)\s+",
                    "",
                    normalized,
                )

                result = cls.differentiate(expression)

                return (
                    f"The derivative is "
                    f"{cls.format_result(result)}."
                )

            if normalized.startswith(
                ("integrate ", "integral of ")
            ):
                expression = re.sub(
                    r"^(integrate|integral of)\s+",
                    "",
                    normalized,
                )

                result = cls.integrate(expression)

                return (
                    f"The integral is "
                    f"{cls.format_result(result)} + C."
                )

            if normalized.startswith(
                ("solve ", "find ")
            ) and "=" in normalized:
                result = cls.solve_equation(normalized)

                return (
                    f"The solution is "
                    f"{cls.format_result(result)}."
                )

            if "=" in normalized:
                result = cls.solve_equation(normalized)

                return (
                    f"The solution is "
                    f"{cls.format_result(result)}."
                )

            result = cls.calculate(text)

            return (
                f"The answer is "
                f"{cls.format_result(result)}."
            )

        except (
            ValueError,
            TypeError,
            SyntaxError,
            ZeroDivisionError,
            OverflowError,
            sp.SympifyError,
            sp.matrices.exceptions.NonSquareMatrixError,
            sp.matrices.exceptions.NonInvertibleMatrixError,
        ):
            return None
