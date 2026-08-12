"""Skill：Agent 可调用的最小执行单元（工具）抽象。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .types import ToolResult


class Skill(ABC):
    """所有工具（Skill）的基类。

    子类需要设置 `name`（唯一标识），可选设置 `description`，
    并实现异步的 `run` 方法承载具体业务逻辑。
    """

    name: str
    description: str = ""

    @abstractmethod
    async def run(self, **kwargs: Any) -> Any:
        """执行工具逻辑，返回原始结果（会被 `execute` 包装为 ToolResult）。"""
        raise NotImplementedError

    async def execute(self, **kwargs: Any) -> ToolResult:
        """执行工具并捕获异常，统一返回 ToolResult，不向上抛出。"""
        try:
            output = await self.run(**kwargs)
            return ToolResult(name=self.name, output=output)
        except Exception as exc:  # noqa: BLE001 - 工具异常需要被统一捕获后返回
            return ToolResult(name=self.name, output=None, error=str(exc))


class SkillRegistry:
    """维护 Skill 名称到实例的映射，提供注册与调度能力。"""

    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        """注册一个 Skill 实例，Skill.name 必须唯一。"""
        if not skill.name:
            raise ValueError("Skill 必须设置 name 属性")
        if skill.name in self._skills:
            raise ValueError(f"Skill '{skill.name}' 已经注册过")
        self._skills[skill.name] = skill

    def get(self, name: str) -> Skill | None:
        """按名称查找 Skill，不存在则返回 None。"""
        return self._skills.get(name)

    def list_skills(self) -> list[str]:
        """返回已注册的 Skill 名称列表。"""
        return list(self._skills.keys())

    async def call(self, name: str, **kwargs: Any) -> ToolResult:
        """按名称路由调用 Skill；Skill 不存在时返回带 error 的 ToolResult。"""
        skill = self.get(name)
        if skill is None:
            return ToolResult(name=name, output=None, error=f"未找到名为 '{name}' 的 Skill")
        return await skill.execute(**kwargs)
