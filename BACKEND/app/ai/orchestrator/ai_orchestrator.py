import json
import re

from app.ai.math.math_engine import MathEngine


class AIOrchestrator:

    @staticmethod
    def _clean_json(text: str):
        text = (text or "").strip()

        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)

        return text.strip()

    @classmethod
    def _parse_json(cls, response: str):
        cleaned = cls._clean_json(response)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            return None

        return data if isinstance(data, dict) else None

    @classmethod
    def build_router_prompt(cls, message: str):
        return f"""
You are the routing component of Velora AI.

Classify the user's request into exactly one route.

Routes:

math
Use for:
- arithmetic
- algebra
- equations
- matrices
- determinants
- matrix inverse
- matrix transpose
- trigonometry
- calculus
- derivatives
- integrals
- logarithms
- mathematical simplification
- numerical calculations
- mathematical word problems
- physics calculations
- chemistry calculations

document
Use when the user asks about:
- an uploaded file
- uploaded PDF
- uploaded document
- uploaded resume
- uploaded CV
- information contained in uploaded material

general
Use for everything else.

Return ONLY valid JSON.

Examples:

{{"route":"math"}}
{{"route":"document"}}
{{"route":"general"}}

User request:
{message}
""".strip()

    @classmethod
    def route(cls, message: str, provider):
        prompt = cls.build_router_prompt(message)
        response = provider.generate_response(prompt=prompt)

        data = cls._parse_json(response)

        if not data:
            return None

        route = data.get("route")

        if route in {"math", "document", "general"}:
            return route

        return None

    @classmethod
    def build_math_instruction_prompt(cls, message: str):
        return f"""
You are the mathematical interpretation component of Velora AI.

Your job is to understand the user's mathematical request and convert it
into a structured instruction for a deterministic mathematics engine.

Do NOT calculate the answer yourself.

Supported operations:

calculate
solve_equation
simplify
differentiate
integrate
matrix_determinant
matrix_inverse
matrix_transpose

Return ONLY valid JSON.

For arithmetic:

{{"operation":"calculate","expression":"14 * 35"}}

For equations:

{{"operation":"solve_equation","expression":"2*x + 5 = 15"}}

For simplification:

{{"operation":"simplify","expression":"(x + 2)^2"}}

For derivatives:

{{"operation":"differentiate","expression":"x^2 + 3*x","variable":"x"}}

For integrals:

{{"operation":"integrate","expression":"x^2","variable":"x"}}

For determinant:

{{"operation":"matrix_determinant","expression":"[[1,2],[3,4]]"}}

For inverse:

{{"operation":"matrix_inverse","expression":"[[1,2],[3,4]]"}}

For transpose:

{{"operation":"matrix_transpose","expression":"[[1,2],[3,4]]"}}

Rules:

- Translate natural language into mathematical notation.
- Preserve all numbers.
- Preserve variables.
- Convert "into", "times", "multiplied by" into multiplication.
- Convert "divided by" into division.
- Convert squared/cubed notation correctly.
- For equations, preserve both sides.
- For matrices, preserve the matrix dimensions and values.
- Do not invent missing values.
- Do not explain anything.
- Return JSON only.

User request:
{message}
""".strip()

    @classmethod
    def interpret_math(cls, message: str, provider):
        prompt = cls.build_math_instruction_prompt(message)
        response = provider.generate_response(prompt=prompt)

        data = cls._parse_json(response)

        if not data:
            return None

        operation = data.get("operation")

        allowed_operations = {
            "calculate",
            "solve_equation",
            "simplify",
            "differentiate",
            "integrate",
            "matrix_determinant",
            "matrix_inverse",
            "matrix_transpose",
        }

        if operation not in allowed_operations:
            return None

        if not data.get("expression"):
            return None

        return data

    @classmethod
    def execute_math(cls, instruction):
        operation = instruction.get("operation")
        expression = instruction.get("expression")
        variable = instruction.get("variable", "x")

        if operation == "calculate":
            result = MathEngine.calculate(expression)
            return f"The answer is {MathEngine.format_result(result)}."

        if operation == "solve_equation":
            result = MathEngine.solve_equation(expression)
            return f"The solution is {MathEngine.format_result(result)}."

        if operation == "simplify":
            result = MathEngine.simplify(expression)
            return f"The simplified expression is {MathEngine.format_result(result)}."

        if operation == "differentiate":
            result = MathEngine.differentiate(
                expression,
                variable=variable,
            )
            return f"The derivative is {MathEngine.format_result(result)}."

        if operation == "integrate":
            result = MathEngine.integrate(
                expression,
                variable=variable,
            )
            return f"The integral is {MathEngine.format_result(result)} + C."

        if operation == "matrix_determinant":
            result = MathEngine.matrix_determinant(expression)
            return f"The determinant is {MathEngine.format_result(result)}."

        if operation == "matrix_inverse":
            result = MathEngine.matrix_inverse(expression)
            return (
                "The inverse is:\n"
                f"{MathEngine.format_result(result)}"
            )

        if operation == "matrix_transpose":
            result = MathEngine.matrix_transpose(expression)
            return (
                "The transpose is:\n"
                f"{MathEngine.format_result(result)}"
            )

        return None

    @classmethod
    def try_math(cls, message: str):
        return MathEngine.answer(message)
