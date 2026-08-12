"""Agent：整合 Memory 与 Skill 的最小可用智能体骨架。"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .memory import InMemoryMemory, Memory
from .skill import SkillRegistry
from .types import Message, Role, ToolCall


class Agent(ABC):
    """Agent 基类。

    子类需要实现 `think` 方法：接收当前记忆中的历史消息，返回：
    - 一段最终自然语言回复（str），或
    - 一个 ToolCall，表示希望调用某个 Skill。

    `run` 方法驱动"感知 -> 决策 -> 执行 -> 反思"的循环，
    直到子类的 `think` 返回自然语言回复，或达到 `max_steps` 上限为止。
    """

    def __init__(
        self,
        skills: SkillRegistry | None = None,
        memory: Memory | None = None,
        max_steps: int = 10,
    ) -> None:
        self.skills = skills or SkillRegistry()
        self.memory = memory or InMemoryMemory()
        self.max_steps = max_steps

    @abstractmethod
    async def think(self, history: list[Message]) -> str | ToolCall:
        """根据历史消息决定下一步动作，由子类实现具体的推理逻辑（如调用 LLM）。"""
        raise NotImplementedError

    async def run(self, user_input: str) -> str:
        """执行一次完整的 Agent 循环，返回最终自然语言回复。"""
        self.memory.add(Message(role=Role.USER, content=user_input))

        for _ in range(self.max_steps):
            decision = await self.think(self.memory.history())

            if isinstance(decision, str):
                self.memory.add(Message(role=Role.ASSISTANT, content=decision))
                return decision

            result = await self.skills.call(decision.name, **decision.arguments)
            tool_message = Message(
                role=Role.TOOL,
                name=decision.name,
                content=str(result.output) if result.ok else f"错误：{result.error}",
            )
            self.memory.add(tool_message)

        return "已达到最大执行步数，未能得出最终结果。"
