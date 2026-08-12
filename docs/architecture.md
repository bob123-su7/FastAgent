# FastAgent 核心包架构说明

本文档介绍 `fastagent/` 包的设计目标、模块划分与扩展方式。

## 设计目标

`fastagent` 是一个**最小可用的 Agent 基础框架**，用于学习和快速搭建 Demo。
它只提供三类核心抽象，不绑定任何具体大模型厂商，也不做多 Agent 编排：

```
Agent = Memory（记忆） + SkillRegistry（工具调度） + think()（决策逻辑）
```

## 模块划分

| 模块 | 文件 | 职责 |
|------|------|------|
| `types` | `fastagent/types.py` | 基于 Pydantic v2 的核心数据类型：`Message`、`Role`、`ToolCall`、`ToolResult` |
| `skill` | `fastagent/skill.py` | `Skill` 抽象基类（工具）与 `SkillRegistry`（注册 + 路由调度） |
| `memory` | `fastagent/memory.py` | `Memory` 抽象基类与 `InMemoryMemory`（进程内、支持滑动窗口截断） |
| `agent` | `fastagent/agent.py` | `Agent` 抽象基类，实现"感知 → 决策 → 执行 → 反思"的循环 |
| `tools` | `fastagent/tools/` | 内置 Skill 示例：`CalculatorSkill`、`ClockSkill`、`ReadFileSkill`、`WriteFileSkill` |

## 核心流程

`Agent.run(user_input)` 的执行流程：

```
写入用户消息到 Memory
    ↓
循环（最多 max_steps 次）：
    think(history) → 自然语言回复 或 ToolCall
        ├─ 若是字符串 → 写入 Memory，作为最终回复返回
        └─ 若是 ToolCall → SkillRegistry.call() 执行对应 Skill
                              → 将结果写回 Memory，继续循环
```

`think` 是唯一需要子类实现的方法，通常在其中调用 LLM（或用规则模拟，见
`examples/calculator_agent.py`），根据历史消息决定下一步是直接回复还是调用工具。

## 如何新增一个 Skill

1. 继承 `fastagent.skill.Skill`，设置 `name`（唯一标识）与可选的 `description`。
2. 实现异步方法 `async def run(self, **kwargs) -> Any`，返回原始结果。
3. 通过 `SkillRegistry.register(...)` 注册后即可被 `Agent` 调用。

```python
from fastagent.skill import Skill

class UpperCaseSkill(Skill):
    name = "upper"
    description = "将文本转换为大写"

    async def run(self, text: str) -> str:
        return text.upper()
```

`Skill.execute()` 会自动捕获 `run()` 中抛出的异常，统一包装为
`ToolResult(error=...)`，调用方无需自行 try/except。

## 如何实现一个 Agent

继承 `fastagent.agent.Agent`，只需实现 `think`：

```python
from fastagent.agent import Agent
from fastagent.types import Message, ToolCall

class MyAgent(Agent):
    async def think(self, history: list[Message]) -> str | ToolCall:
        # 在这里调用 LLM，解析其输出，
        # 返回字符串（直接回复）或 ToolCall（请求调用某个 Skill）
        ...
```

## 与 `docs/harness技术介绍及运用.md` 的关系

该文档描述的 Harness 是更重的"多 Agent 调度中枢"概念（会话生命周期管理、
多 Agent 任务分发、可观测性等），而本包中的 `SkillRegistry` 只是其中
"Skill 统一调度入口"职责的最小实现，二者不冲突，`SkillRegistry` 可以
作为未来实现完整 Harness 的基础构件之一。

## 测试

单元测试位于 `tests/`，覆盖 `skill`、`memory`、`agent`、内置 `tools` 四个模块。

```bash
pip install -r requirements.txt
pytest
```
