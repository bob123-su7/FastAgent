"""内置 Skill 集合（fastagent.tools）单元测试。"""

import pytest

from fastagent.tools import CalculatorSkill, ClockSkill, ReadFileSkill, WriteFileSkill
from fastagent.tools.calculator import safe_eval


def test_safe_eval_basic_arithmetic():
    assert safe_eval("1 + 2 * (3 - 1)") == 5


def test_safe_eval_rejects_unsupported_syntax():
    with pytest.raises(Exception):
        safe_eval("__import__('os').system('echo hi')")


@pytest.mark.asyncio
async def test_calculator_skill_run():
    skill = CalculatorSkill()

    result = await skill.execute(expression="2 ** 3")

    assert result.ok
    assert result.output == 8


@pytest.mark.asyncio
async def test_clock_skill_returns_iso_string_by_default():
    skill = ClockSkill()

    result = await skill.execute()

    assert result.ok
    assert "T" in result.output


@pytest.mark.asyncio
async def test_write_then_read_file_roundtrip(tmp_path):
    write_skill = WriteFileSkill(root=tmp_path)
    read_skill = ReadFileSkill(root=tmp_path)

    write_result = await write_skill.execute(path="note.txt", content="hello fastagent")
    read_result = await read_skill.execute(path="note.txt")

    assert write_result.ok
    assert read_result.ok
    assert read_result.output == "hello fastagent"


@pytest.mark.asyncio
async def test_file_skill_rejects_path_outside_root(tmp_path):
    read_skill = ReadFileSkill(root=tmp_path)

    result = await read_skill.execute(path="../outside.txt")

    assert not result.ok
    assert "超出允许的根目录范围" in result.error
