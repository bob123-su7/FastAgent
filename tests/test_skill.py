"""Skill / SkillRegistry 单元测试。"""

import pytest

from fastagent.skill import Skill, SkillRegistry


class EchoSkill(Skill):
    name = "echo"
    description = "原样返回输入内容"

    async def run(self, text: str) -> str:
        return text


class FailingSkill(Skill):
    name = "boom"

    async def run(self) -> None:
        raise RuntimeError("造成异常")


@pytest.mark.asyncio
async def test_register_and_call_skill():
    registry = SkillRegistry()
    registry.register(EchoSkill())

    result = await registry.call("echo", text="hello")

    assert result.ok
    assert result.output == "hello"


@pytest.mark.asyncio
async def test_call_unknown_skill_returns_error():
    registry = SkillRegistry()

    result = await registry.call("missing")

    assert not result.ok
    assert "missing" in result.error


@pytest.mark.asyncio
async def test_skill_execution_error_is_captured():
    registry = SkillRegistry()
    registry.register(FailingSkill())

    result = await registry.call("boom")

    assert not result.ok
    assert "造成异常" in result.error


def test_duplicate_registration_raises():
    registry = SkillRegistry()
    registry.register(EchoSkill())

    with pytest.raises(ValueError):
        registry.register(EchoSkill())


def test_list_skills_returns_registered_names():
    registry = SkillRegistry()
    registry.register(EchoSkill())
    registry.register(FailingSkill())

    assert set(registry.list_skills()) == {"echo", "boom"}
