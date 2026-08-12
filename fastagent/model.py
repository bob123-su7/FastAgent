"""Model interface for agents backed by a provider."""

from __future__ import annotations

from typing import Protocol

from .agent import Agent
from .memory import Memory
from .skill import SkillRegistry
from .types import Message, ToolCall


class Model(Protocol):
    """Produces an agent's next decision from its conversation history."""

    async def complete(self, messages: list[Message]) -> str | ToolCall: ...


class ModelAgent(Agent):
    """An Agent whose decisions come from a Model."""

    def __init__(
        self,
        model: Model,
        skills: SkillRegistry | None = None,
        memory: Memory | None = None,
        max_steps: int = 10,
    ) -> None:
        super().__init__(skills=skills, memory=memory, max_steps=max_steps)
        self.model = model

    async def think(self, history: list[Message]) -> str | ToolCall:
        return await self.model.complete(history)
