"""Agent 循环逻辑单元测试。"""

import pytest

from fastagent.agent import Agent
from fastagent.skill import Skill, SkillRegistry
from fastagent.types import Message, Role, ToolCall


class AddSkill(Skill):
    name = "add"

    async def run(self, a: int, b: int) -> int:
        return a + b


class ScriptedAgent(Agent):
    """按预设脚本依次返回动作，用于测试 Agent 循环逻辑，无需真实 LLM。"""

    def __init__(self, script: list, **kwargs):
        super().__init__(**kwargs)
        self._script = list(script)

    async def think(self, history: list[Message]):
        return self._script.pop(0)


@pytest.mark.asyncio
async def test_agent_returns_direct_reply():
    agent = ScriptedAgent(script=["你好！"])

    reply = await agent.run("嗨")

    assert reply == "你好！"
    assert agent.memory.history()[-1].content == "你好！"


@pytest.mark.asyncio
async def test_agent_calls_skill_then_replies():
    registry = SkillRegistry()
    registry.register(AddSkill())

    agent = ScriptedAgent(
        script=[ToolCall(name="add", arguments={"a": 1, "b": 2}), "结果是 3"],
        skills=registry,
    )

    reply = await agent.run("帮我算 1+2")

    assert reply == "结果是 3"
    tool_messages = [m for m in agent.memory.history() if m.role == Role.TOOL]
    assert tool_messages[0].content == "3"


@pytest.mark.asyncio
async def test_agent_stops_after_max_steps():
    agent = ScriptedAgent(
        script=[ToolCall(name="missing", arguments={})] * 5,
        max_steps=2,
    )

    reply = await agent.run("测试")

    assert "最大执行步数" in reply
