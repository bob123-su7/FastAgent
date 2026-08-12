"""Memory 单元测试。"""

from fastagent.memory import InMemoryMemory
from fastagent.types import Message, Role


def test_add_and_history_preserves_order():
    memory = InMemoryMemory()
    memory.add(Message(role=Role.USER, content="第一条"))
    memory.add(Message(role=Role.ASSISTANT, content="第二条"))

    history = memory.history()

    assert [m.content for m in history] == ["第一条", "第二条"]


def test_max_messages_truncates_oldest():
    memory = InMemoryMemory(max_messages=2)
    memory.add(Message(role=Role.USER, content="1"))
    memory.add(Message(role=Role.USER, content="2"))
    memory.add(Message(role=Role.USER, content="3"))

    history = memory.history()

    assert [m.content for m in history] == ["2", "3"]


def test_clear_empties_history():
    memory = InMemoryMemory()
    memory.add(Message(role=Role.USER, content="x"))
    memory.clear()

    assert memory.history() == []


def test_history_returns_copy_not_reference():
    memory = InMemoryMemory()
    memory.add(Message(role=Role.USER, content="x"))

    history = memory.history()
    history.append(Message(role=Role.USER, content="y"))

    assert len(memory.history()) == 1
