"""内置 Skill（工具）集合，开箱即用，方便学习与快速搭建 Demo。"""

from .calculator import CalculatorSkill
from .clock import ClockSkill
from .file_io import ReadFileSkill, WriteFileSkill

__all__ = [
    "CalculatorSkill",
    "ClockSkill",
    "ReadFileSkill",
    "WriteFileSkill",
]
