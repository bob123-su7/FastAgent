"""计算器 Skill：安全地计算一个数学表达式字符串。"""

from __future__ import annotations

import ast
import operator
from typing import Any

from ..skill import Skill

_ALLOWED_BINOPS: dict[type, Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_ALLOWED_UNARYOPS: dict[type, Any] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _eval_node(node: ast.AST) -> float:
    """递归求值 AST 节点，只允许数字与基本算术运算，杜绝任意代码执行。"""
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"不支持的常量类型：{node.value!r}")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_BINOPS:
            raise ValueError(f"不支持的运算符：{op_type.__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_BINOPS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARYOPS:
            raise ValueError(f"不支持的运算符：{op_type.__name__}")
        return _ALLOWED_UNARYOPS[op_type](_eval_node(node.operand))

    raise ValueError(f"不支持的表达式节点：{type(node).__name__}")


def safe_eval(expression: str) -> float:
    """安全地计算只包含数字与 + - * / // % ** () 的算术表达式。"""
    parsed = ast.parse(expression, mode="eval")
    return _eval_node(parsed.body)


class CalculatorSkill(Skill):
    """计算数学表达式的 Skill，例如 "1 + 2 * (3 - 1)"。"""

    name = "calculator"
    description = "计算一个只包含数字与 + - * / // % ** () 的算术表达式"

    async def run(self, expression: str) -> float:
        return safe_eval(expression)
