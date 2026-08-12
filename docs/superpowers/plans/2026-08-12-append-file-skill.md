# AppendFileSkill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a sandboxed built-in skill that appends UTF-8 text to files and is covered by behavior-focused tests.

**Architecture:** Extend the existing `fastagent.tools.file_io` module so the new skill shares the same root-path containment helper and execution/error wrapper as the read and write skills. Export it through `fastagent.tools` and validate observable filesystem behavior with real temporary directories.

**Tech Stack:** Python 3.10+, pathlib, pytest, pytest-asyncio

## Global Constraints

- Do not add third-party dependencies.
- Preserve all existing public interfaces.
- Reject paths outside the configured root directory.
- Read and write text as UTF-8.

---

### Task 1: AppendFileSkill behavior and public export

Execution note: the local environment did not have `pytest-asyncio` installed, so the new tests use `asyncio.run()` and execute under plain pytest instead of being skipped.

**Files:**
- Modify: `tests/test_tools.py`
- Modify: `fastagent/tools/file_io.py`
- Modify: `fastagent/tools/__init__.py`

**Interfaces:**
- Consumes: `_resolve_within_root(root: Path, relative_path: str) -> Path` and `Skill.execute(**kwargs) -> SkillResult`
- Produces: `AppendFileSkill(root: str | Path = ".")` with `async run(path: str, content: str) -> str`

- [x] **Step 1: Write failing behavior tests**

Add imports and tests that exercise the real filesystem:

```python
from fastagent.tools import AppendFileSkill, CalculatorSkill, ClockSkill, ReadFileSkill, WriteFileSkill

@pytest.mark.asyncio
async def test_append_file_preserves_existing_content_and_creates_parent(tmp_path):
    append_skill = AppendFileSkill(root=tmp_path)
    read_skill = ReadFileSkill(root=tmp_path)

    first = await append_skill.execute(path="logs/agent.txt", content="first\n")
    second = await append_skill.execute(path="logs/agent.txt", content="second\n")
    read_result = await read_skill.execute(path="logs/agent.txt")

    assert first.ok
    assert second.ok
    assert read_result.output == "first\nsecond\n"

@pytest.mark.asyncio
async def test_append_file_rejects_path_outside_root(tmp_path):
    append_skill = AppendFileSkill(root=tmp_path)

    result = await append_skill.execute(path="../outside.txt", content="blocked")

    assert not result.ok
    assert "超出允许的根目录范围" in result.error
    assert not (tmp_path.parent / "outside.txt").exists()
```

- [x] **Step 2: Run tests and verify RED**

Run: `python -m pytest tests/test_tools.py -q`

Expected: collection fails because `AppendFileSkill` is not exported.

- [x] **Step 3: Implement the minimal skill and export it**

Add to `fastagent/tools/file_io.py`:

```python
class AppendFileSkill(Skill):
    """向根目录下某个文本文件追加内容，不存在时创建文件。"""

    name = "append_file"
    description = "向指定根目录下某个文本文件追加内容，参数为相对路径 path 与文本 content"

    def __init__(self, root: str | Path = ".") -> None:
        self._root = Path(root)

    async def run(self, path: str, content: str) -> str:
        target = _resolve_within_root(self._root, path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as file:
            file.write(content)
        return f"已追加 {target}"
```

Import `AppendFileSkill` in `fastagent/tools/__init__.py` and add it to `__all__`.

- [x] **Step 4: Run focused and complete tests**

Run: `python -m pytest tests/test_tools.py -q`

Expected: all tool tests pass.

Run: `python -m pytest -q`

Expected: the complete suite passes.

- [x] **Step 5: Check and commit**

Run: `git diff --check`

Expected: no output.

Commit the plan, tests, implementation, and export with `feat: add append file skill`.
