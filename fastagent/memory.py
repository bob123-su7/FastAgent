"""Memory：维护 Agent 的会话上下文。"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .types import Message


class Memory(ABC):
    """记忆模块基类。"""

    @abstractmethod
    def add(self, message: Message) -> None:
        """写入一条消息。"""

    @abstractmethod
    def history(self) -> list[Message]:
        """读取当前记忆中的全部消息，按时间顺序返回。"""

    def clear(self) -> None:
        """清空记忆。默认不实现，由具体子类决定是否支持。"""
        raise NotImplementedError


class InMemoryMemory(Memory):
    """最简单的记忆实现：进程内列表，支持可选的最大长度截断（滑动窗口）。"""

    def __init__(self, max_messages: int | None = None) -> None:
        self._messages: list[Message] = []
        self._max_messages = max_messages

    def add(self, message: Message) -> None:
        self._messages.append(message)
        if self._max_messages is not None and len(self._messages) > self._max_messages:
            self._messages = self._messages[-self._max_messages :]

    def history(self) -> list[Message]:
        return list(self._messages)

    def clear(self) -> None:
        self._messages.clear()
