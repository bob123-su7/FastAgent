"""FastAgent 核心包。

提供构建 AI Agent 所需的基础抽象：
- Skill（工具）：Agent 可调用的最小执行单元
- Memory（记忆）：维护会话上下文
- Agent（智能体）：整合感知、决策、执行的推理循环
"""

from .agent import Agent
from .memory import InMemoryMemory, Memory
from .skill import Skill, SkillRegistry
from .tracer import AgentTracer, TraceSpan
from .types import Message, Role, ToolCall, ToolResult

__version__ = "0.1.0"

__all__ = [
    "Agent",
    "AgentTracer",
    "InMemoryMemory",
    "Memory",
    "Message",
    "Role",
    "Skill",
    "SkillRegistry",
    "ToolCall",
    "ToolResult",
    "TraceSpan",
    "__version__",
]
