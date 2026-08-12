"""FastAgent 核心数据类型，基于 Pydantic v2 定义。"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Role(str, Enum):
    """对话消息角色。"""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Message(BaseModel):
    """一条对话消息。"""

    role: Role
    content: str
    name: str | None = None


class ToolCall(BaseModel):
    """LLM / Agent 请求调用某个工具（Skill）的指令。"""

    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    """工具（Skill）执行后的结果。"""

    name: str
    output: Any = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        """执行是否成功（无异常）。"""
        return self.error is None
